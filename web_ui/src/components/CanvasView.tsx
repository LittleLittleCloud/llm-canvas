import dagre from "dagre";
import React, { useCallback, useMemo, useRef } from "react";
import ReactFlow, {
  Background,
  ConnectionMode,
  Controls,
  Edge,
  Handle,
  MarkerType,
  MiniMap,
  Node,
  Panel,
  Position,
  ReactFlowProvider,
  useEdgesState,
  useNodes,
  useNodesState,
} from "reactflow";
import "reactflow/dist/style.css";
import { CanvasData, MessageNode } from "../types";
import { MessageNodeComponent } from "./MessageNode";

interface Props {
  data: CanvasData;
}

// Custom node component for React Flow
const CustomMessageNode = ({
  data,
  selected,
}: {
  data: MessageNode & {
    hasParent?: boolean;
    hasChildren?: boolean;
    direction?: string;
  };
  selected?: boolean;
}) => {
  const { hasParent = false, hasChildren = false, direction = "TB" } = data;
  const isVertical = direction === "TB";
  const nodeRef = useRef<HTMLDivElement>(null);

  // Get all nodes and find the current node instance
  const nodes = useNodes();
  const currentNode = nodes.find(node => node.id === data.id);

  // Add data attribute for easier DOM querying
  return (
    <div
      ref={nodeRef}
      data-node-id={data.id}
      className={`nowheel bg-white rounded-lg shadow-md border-2 min-w-[280px] relative transition-all duration-200 ${
        selected
          ? "border-blue-500 shadow-lg ring-2 ring-blue-200"
          : "border-gray-200 hover:border-gray-300"
      }`}
    >
      {/* Target handle - only show if node has parent */}
      {hasParent && (
        <Handle
          type="target"
          position={isVertical ? Position.Top : Position.Left}
          id={isVertical ? "top" : "left"}
          style={{ background: "#6366f1" }}
          isConnectable={false}
        />
      )}

      <MessageNodeComponent node={data} />

      {/* Dimensions display */}
      <div className="absolute top-1 right-1 bg-gray-100 text-gray-600 text-xs px-1 py-0.5 rounded opacity-70">
        {currentNode?.width}×{currentNode?.height}
        {currentNode && (
          <div className="text-xs">
            Pos: {Math.round(currentNode.position.x)},
            {Math.round(currentNode.position.y)}
          </div>
        )}
      </div>

      {/* Source handle - only show if node has children */}
      {hasChildren && (
        <Handle
          type="source"
          position={isVertical ? Position.Bottom : Position.Right}
          id={isVertical ? "bottom" : "right"}
          style={{ background: "#6366f1" }}
          isConnectable={false}
        />
      )}
    </div>
  );
};

// Define nodeTypes outside component to prevent recreation on every render
const nodeTypes = {
  messageNode: CustomMessageNode,
};

// Dagre layout configuration
const dagreGraph = new dagre.graphlib.Graph();
dagreGraph.setDefaultEdgeLabel(() => ({}));

const getLayoutedElements = (
  nodes: Node[],
  edges: Edge[],
  direction = "TB",
  dataNodes: Record<string, MessageNode> = {}
) => {
  const isVertical = direction === "TB";

  // Function to get node dimensions with fallbacks
  const getNodeDimensions = (node: Node) => {
    const baseWidth = 320;
    const baseHeight = 150;

    // Try to use existing width/height from node
    if (node.width && node.height && node.width > 0 && node.height > 0) {
      return {
        width: node.width,
        height: node.height,
      };
    }

    // Try to get dimensions from DOM
    const nodeElement = document.querySelector(`[data-node-id="${node.id}"]`);
    if (nodeElement) {
      const rect = nodeElement.getBoundingClientRect();
      if (rect.width > 0 && rect.height > 0) {
        return {
          width: Math.max(rect.width, baseWidth),
          height: Math.max(rect.height, baseHeight),
        };
      }
    }

    // Fallback: estimate based on content
    const messageNode = dataNodes[node.id];
    if (messageNode) {
      const content = messageNode.content.content;
      let contentLength = 0;

      if (typeof content === "string") {
        contentLength = content.length;
      } else if (Array.isArray(content)) {
        contentLength = content.reduce((total, block) => {
          if ("text" in block && typeof block.text === "string") {
            return total + block.text.length;
          }
          return total + JSON.stringify(block).length;
        }, 0);
      }

      const lines = Math.ceil(contentLength / 80);
      const estimatedHeight = Math.max(baseHeight, 120 + lines * 20);

      return {
        width: baseWidth,
        height: Math.min(estimatedHeight, 400),
      };
    }

    // Final fallback
    return { width: baseWidth, height: baseHeight };
  };

  dagreGraph.setGraph({
    rankdir: direction,
    nodesep: 50,
    ranksep: 100,
    marginx: 50,
    marginy: 50,
  });

  // Set nodes with calculated dimensions
  nodes.forEach(node => {
    const dimensions = getNodeDimensions(node);
    dagreGraph.setNode(node.id, dimensions);

    // Update node with dimensions for later use
    node.width = dimensions.width;
    node.height = dimensions.height;
  });

  edges.forEach(edge => {
    dagreGraph.setEdge(edge.source, edge.target);
  });

  dagre.layout(dagreGraph);

  nodes.forEach(node => {
    // Now we're guaranteed to have width and height
    const nodeWithPosition = dagreGraph.node(node.id);
    const originalNode = dataNodes[node.id];

    // Determine if node has parent and children
    const hasParent = originalNode?.parent_id != null;
    const hasChildren = originalNode?.child_ids?.length > 0;

    node.targetPosition = isVertical ? Position.Top : Position.Left;
    node.sourcePosition = isVertical ? Position.Bottom : Position.Right;
    node.position = {
      x: nodeWithPosition.x - node.width! / 2,
      y: nodeWithPosition.y - node.height! / 2,
    };

    // Update node data with handle information
    node.data = {
      ...node.data,
      hasParent,
      hasChildren,
      direction,
    };
  });

  // Update edges with correct handle IDs
  const updatedEdges = edges.map(edge => ({
    ...edge,
    sourceHandle: isVertical ? "bottom" : "right",
    targetHandle: isVertical ? "top" : "left",
  }));

  return { nodes, edges: updatedEdges };
};

export const CanvasView: React.FC<Props> = ({ data }) => {
  const { nodes: initialNodes, edges: initialEdges } = useMemo(() => {
    const nodes: Node[] = [];
    const edges: Edge[] = [];

    // Create nodes with parent/children information
    Object.entries(data.nodes).forEach(([nodeId, node]) => {
      const hasParent = node.parent_id != null;
      const hasChildren = node.child_ids.length > 0;

      nodes.push({
        id: nodeId,
        type: "messageNode",
        position: { x: 0, y: 0 }, // Will be set by layout
        data: {
          ...node,
          hasParent,
          hasChildren,
          direction: "TB",
        },
        style: { width: 300 },
      });
    });

    // Create edges
    Object.entries(data.nodes).forEach(([nodeId, node]) => {
      node.child_ids.forEach(childId => {
        edges.push({
          id: `${nodeId}-${childId}`,
          source: nodeId,
          target: childId,
          sourceHandle: "bottom",
          targetHandle: "top",
          type: "smoothstep",
          animated: false,
          style: {
            stroke: "#6366f1",
            strokeWidth: 2,
          },
          markerEnd: {
            type: MarkerType.ArrowClosed,
            width: 20,
            height: 20,
            color: "#6366f1",
          },
        });
      });
    });

    // Apply automatic layout
    return getLayoutedElements(nodes, edges, "TB", data.nodes);
  }, [data]);

  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  // Enhanced layout function that can use React Flow's getNodes for actual dimensions
  const onLayout = useCallback(
    (direction: string) => {
      // Update nodes with new direction information
      const updatedNodes = nodes.map(node => ({
        ...node,
        data: {
          ...node.data,
          direction,
        },
      }));

      const { nodes: layoutedNodes, edges: layoutedEdges } =
        getLayoutedElements(updatedNodes, edges, direction, data.nodes);

      setNodes([...layoutedNodes]);
      setEdges([...layoutedEdges]);
    },
    [nodes, edges, setNodes, setEdges, data.nodes]
  );

  const onReLayout = useCallback(() => {
    // Get current direction from the first node, default to TB
    const currentDirection = nodes[0]?.data?.direction || "TB";
    onLayout(currentDirection);
  }, [nodes, onLayout]);

  return (
    <div className="h-full w-full">
      <ReactFlowProvider>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          nodeTypes={nodeTypes}
          connectionMode={ConnectionMode.Loose}
          fitView
          fitViewOptions={{ padding: 0.1 }}
          className="bg-gray-50"
          defaultEdgeOptions={{
            type: "smoothstep",
            animated: false,
            style: { strokeWidth: 2, stroke: "#6366f1" },
            markerEnd: { type: MarkerType.ArrowClosed, color: "#6366f1" },
          }}
          deleteKeyCode={["Backspace", "Delete"]}
          multiSelectionKeyCode={["Meta", "Ctrl"]}
        >
          <Background color="#f3f4f6" gap={20} />
          <Controls />
          <MiniMap
            nodeColor="#6366f1"
            maskColor="rgba(0, 0, 0, 0.1)"
            className="!bg-white !border-gray-300"
          />
          <Panel
            position="top-left"
            className="bg-white p-3 rounded-lg shadow text-sm space-y-2"
          >
            <div className="font-semibold text-gray-800">
              {data.title || "Canvas"}
            </div>
            <div className="text-gray-500">
              {Object.keys(data.nodes).length} messages
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => onLayout("TB")}
                className="px-2 py-1 text-xs bg-blue-500 text-white rounded hover:bg-blue-600"
              >
                ⬇ Vertical
              </button>
              <button
                onClick={() => onLayout("LR")}
                className="px-2 py-1 text-xs bg-blue-500 text-white rounded hover:bg-blue-600"
              >
                ➡ Horizontal
              </button>
              <button
                onClick={onReLayout}
                className="px-2 py-1 text-xs bg-green-500 text-white rounded hover:bg-green-600"
              >
                🔄 Re-layout
              </button>
            </div>
          </Panel>
        </ReactFlow>
      </ReactFlowProvider>
    </div>
  );
};
