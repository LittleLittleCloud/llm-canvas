import dagre from "dagre";
import React, { useCallback, useEffect, useRef } from "react";
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
  useReactFlow,
} from "reactflow";
import "reactflow/dist/style.css";
import { useCanvasStore } from "../store/canvasStore";
import { MessageNode } from "../types";
import { MessageNodeComponent } from "./MessageNode";

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
      className={`bg-white rounded-lg shadow-md border-2 min-w-[280px] relative transition-all duration-200 ${
        selected
          ? "nowheel border-blue-500 shadow-lg ring-2 ring-blue-200"
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
          width: rect.width,
          height: rect.height,
        };
      }
    }

    throw new Error(`Node ${node.id} has no valid dimensions`);
  };

  dagreGraph.setGraph({
    rankdir: direction,
    nodesep: 50,
    ranksep: 100,
    marginx: 10,
    marginy: 10,
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

export const CanvasView: React.FC = () => {
  return (
    <div className="h-full w-full">
      <ReactFlowProvider>
        <CanvasViewInner />
      </ReactFlowProvider>
    </div>
  );
};

const CanvasViewInner: React.FC = () => {
  const data = useCanvasStore(s => s.canvas);
  const reactFlowInstance = useReactFlow();
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  useEffect(() => {
    if (!data) {
      setNodes([]);
      setEdges([]);
      return;
    }
    const nodes: Node[] = [];
    const edges: Edge[] = [];

    // Create nodes with parent/children information
    Object.entries(data.nodes).forEach(([nodeId, node]) => {
      const hasParent = node.parent_id != null;
      const hasChildren = node.child_ids.length > 0;

      nodes.push({
        id: `${nodeId}`,
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

    setNodes(nodes);
    setEdges(edges);
  }, [data, setNodes, setEdges]);

  // Separate effect to trigger re-layout after nodes are set
  useEffect(() => {
    if (nodes.length > 0 && data) {
      // Use setTimeout to ensure nodes are rendered before layout
      const timeoutId = setTimeout(() => {
        // Get current direction from the first node, default to TB
        const currentDirection = nodes[0]?.data?.direction || "TB";
        const { nodes: layoutedNodes, edges: layoutedEdges } =
          getLayoutedElements(nodes, edges, currentDirection, data.nodes);

        setNodes([...layoutedNodes]);
        setEdges([...layoutedEdges]);

        // Center the view on the root node
        // find the root nodes from data.nodes
        // a root node is one that has no parent_id
        const root_ids = Object.values(data.nodes)
          .filter(node => node.parent_id == null)
          .map(node => node.id);
        const rootNode = layoutedNodes.find(node => node.id === root_ids[0]);
        if (rootNode) {
          const x = rootNode.position.x + (rootNode.width || 300) / 2;
          const y = rootNode.position.y + (rootNode.height || 150) / 2;
          reactFlowInstance.setCenter(x, y, {
            zoom: reactFlowInstance.getZoom(),
            duration: 800,
          });
        }
      }, 100);

      return () => clearTimeout(timeoutId);
    }
  }, [nodes.length, data]); // Only trigger when nodes.length changes and we have data

  // Node navigation functions
  const shakeNode = useCallback((nodeId: string) => {
    const nodeElement = document.querySelector(`[data-node-id="${nodeId}"]`);
    if (nodeElement) {
      nodeElement.classList.add("animate-shake");
      setTimeout(() => {
        nodeElement.classList.remove("animate-shake");
      }, 500);
    }
  }, []);

  const selectNode = useCallback(
    (nodeId: string) => {
      setNodes(nodes =>
        nodes.map(node => ({
          ...node,
          selected: node.id === nodeId,
        }))
      );

      // Check if the selected node is outside the current viewport
      const selectedNode = nodes.find(n => n.id === nodeId);
      if (selectedNode && reactFlowInstance) {
        const viewport = reactFlowInstance.getViewport();

        // Get the actual flow container dimensions
        const flowContainer = document.querySelector(".react-flow__viewport");
        const containerRect = flowContainer?.getBoundingClientRect();

        if (containerRect) {
          const containerWidth = containerRect.width;
          const containerHeight = containerRect.height;

          // Transform node coordinates to screen coordinates
          const nodeLeft = selectedNode.position.x * viewport.zoom + viewport.x;
          const nodeTop = selectedNode.position.y * viewport.zoom + viewport.y;
          const nodeRight =
            nodeLeft + (selectedNode.width || 300) * viewport.zoom;
          const nodeBottom =
            nodeTop + (selectedNode.height || 150) * viewport.zoom;

          // Check if any part of the node is outside the viewport
          const isOutsideViewport =
            nodeLeft < 0 ||
            nodeTop < 0 ||
            nodeRight > containerWidth ||
            nodeBottom > containerHeight;

          if (isOutsideViewport) {
            const x = selectedNode.position.x + (selectedNode.width || 300) / 2;
            const y =
              selectedNode.position.y + (selectedNode.height || 150) / 2;

            // Use setCenter to smoothly animate to the selected node
            reactFlowInstance.setCenter(x, y, {
              zoom: reactFlowInstance.getZoom(),
              duration: 800,
            });
          }
        }
      }
    },
    [setNodes, nodes, reactFlowInstance]
  );

  const findClosestNode = useCallback(
    (currentNodeId: string, direction: "up" | "down" | "left" | "right") => {
      const currentNode = nodes.find(n => n.id === currentNodeId);
      if (!currentNode) return null;

      const currentX = currentNode.position.x + (currentNode.width || 300) / 2;
      const currentY = currentNode.position.y + (currentNode.height || 150) / 2;

      let candidates = nodes.filter(n => n.id !== currentNodeId);

      // Filter candidates based on direction
      switch (direction) {
        case "up":
          candidates = candidates.filter(n => {
            const nodeY = n.position.y + (n.height || 150) / 2;
            return nodeY < currentY;
          });
          break;
        case "down":
          candidates = candidates.filter(n => {
            const nodeY = n.position.y + (n.height || 150) / 2;
            return nodeY > currentY;
          });
          break;
        case "left":
          candidates = candidates.filter(n => {
            const nodeX = n.position.x + (n.width || 300) / 2;
            return nodeX < currentX;
          });
          break;
        case "right":
          candidates = candidates.filter(n => {
            const nodeX = n.position.x + (n.width || 300) / 2;
            return nodeX > currentX;
          });
          break;
      }

      if (candidates.length === 0) return null;

      // Find the closest candidate
      let closest = candidates[0];
      let minDistance = Infinity;

      candidates.forEach(candidate => {
        const candidateX = candidate.position.x + (candidate.width || 300) / 2;
        const candidateY = candidate.position.y + (candidate.height || 150) / 2;

        let distance: number;

        switch (direction) {
          case "up":
          case "down":
            // For vertical movement, prioritize Y distance but consider X distance for ties
            distance =
              Math.abs(candidateY - currentY) +
              Math.abs(candidateX - currentX) * 0.1;
            break;
          case "left":
          case "right":
            // For horizontal movement, prioritize X distance but consider Y distance for ties
            distance =
              Math.abs(candidateX - currentX) +
              Math.abs(candidateY - currentY) * 0.1;
            break;
          default:
            distance = Math.sqrt(
              Math.pow(candidateX - currentX, 2) +
                Math.pow(candidateY - currentY, 2)
            );
        }

        if (distance < minDistance) {
          minDistance = distance;
          closest = candidate;
        }
      });

      return closest;
    },
    [nodes]
  );

  const handleKeyDown = useCallback(
    (event: KeyboardEvent) => {
      // Only handle arrow keys and only if focus is on the flow
      if (
        !["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"].includes(event.key)
      ) {
        return;
      }

      // Check if any input/textarea is focused
      const activeElement = document.activeElement;
      if (
        activeElement &&
        (activeElement.tagName === "INPUT" ||
          activeElement.tagName === "TEXTAREA")
      ) {
        return;
      }

      event.preventDefault();

      const selectedNode = nodes.find(n => n.selected);
      if (!selectedNode) {
        // If no node is selected, select the first one
        if (nodes.length > 0) {
          selectNode(nodes[0].id);
        }
        return;
      }

      let direction: "up" | "down" | "left" | "right";
      switch (event.key) {
        case "ArrowUp":
          direction = "up";
          break;
        case "ArrowDown":
          direction = "down";
          break;
        case "ArrowLeft":
          direction = "left";
          break;
        case "ArrowRight":
          direction = "right";
          break;
        default:
          return;
      }

      const closestNode = findClosestNode(selectedNode.id, direction);
      if (closestNode) {
        selectNode(closestNode.id);
      } else {
        // No node found in that direction, shake the current node
        shakeNode(selectedNode.id);
      }
    },
    [nodes, selectNode, findClosestNode, shakeNode]
  );

  // Add keyboard event listener
  useEffect(() => {
    document.addEventListener("keydown", handleKeyDown);
    return () => {
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [handleKeyDown]);

  const handleNodeClick = useCallback(
    (event: React.MouseEvent, node: Node) => {
      selectNode(node.id);
    },
    [selectNode]
  );

  const handlePaneClick = useCallback(() => {
    // Deselect all nodes when clicking on empty space
    setNodes(nodes =>
      nodes.map(node => ({
        ...node,
        selected: false,
      }))
    );
  }, [setNodes]);

  // Enhanced layout function that can use React Flow's getNodes for actual dimensions
  const onLayout = useCallback(
    (direction: string) => {
      if (!data) return;

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
    [nodes, edges, setNodes, setEdges, data]
  );

  const onReLayout = useCallback(() => {
    // Get current direction from the first node, default to TB
    const currentDirection = nodes[0]?.data?.direction || "TB";
    onLayout(currentDirection);
  }, [nodes, onLayout]);

  return (
    <ReactFlow
      nodes={nodes}
      edges={edges}
      onNodesChange={onNodesChange}
      onEdgesChange={onEdgesChange}
      onNodeClick={handleNodeClick}
      onPaneClick={handlePaneClick}
      nodeTypes={nodeTypes}
      connectionMode={ConnectionMode.Loose}
      disableKeyboardA11y
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
      tabIndex={0}
      style={{ outline: "none" }}
    >
      <Background color="#f3f4f6" gap={20} />
      <Controls />
      <MiniMap
        pannable
        zoomable
        nodeColor="#6366f1"
        maskColor="rgba(0, 0, 0, 0.1)"
        className="!bg-white !border-gray-300"
      />
      <Panel
        position="top-left"
        className="bg-white p-3 rounded-lg shadow text-sm space-y-2"
      >
        <div className="font-semibold text-gray-800">
          {data?.title || "Canvas"}
        </div>
        <div className="text-gray-500">
          {data ? Object.keys(data.nodes).length : 0} messages
        </div>
        <div className="text-xs text-gray-400 mb-2">
          Use ↑↓←→ arrow keys to navigate between nodes
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
  );
};
