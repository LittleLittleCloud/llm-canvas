import dagre from "dagre";
import React, { useCallback, useEffect, useRef } from "react";
import ReactFlow, {
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
  useNodesState,
  useReactFlow,
} from "reactflow";
import "reactflow/dist/style.css";
import { CanvasData, MessageNode } from "../types";
import { MessageNodeComponent } from "./MessageNode";

// Define the Canvas type based on the structure used in the store
// Props interface for the CanvasView component
export interface CanvasViewProps {
  canvas?: CanvasData;
  showMiniMap?: boolean;
  showControls?: boolean;
  showPanel?: boolean;
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

  // Add data attribute for easier DOM querying
  return (
    <div
      ref={nodeRef}
      data-node-id={data.id}
      className={`bg-white dark:bg-gray-800 shadow-sm hover:shadow-xl border border-gray-100 dark:border-gray-700 min-w-[320px] relative transition-all duration-300 hover:scale-[1.02] group ${
        selected
          ? "nowheel nopan"
          : "hover:border-indigo-200 dark:hover:border-indigo-600"
      }`}
    >
      {/* header ribbon */}
      <div
        className={`h-1 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 rounded-t-2xl transition-opacity duration-300 ${
          selected ? "opacity-100" : "opacity-0"
        }`}
      />
      {/* Node content */}
      {/* Target handle - only show if node has parent */}
      {hasParent && (
        <Handle
          type="target"
          position={isVertical ? Position.Top : Position.Left}
          id={isVertical ? "top" : "left"}
          style={{
            background: "linear-gradient(135deg, #6366f1, #8b5cf6)",
            border: "2px solid white",
            width: "12px",
            height: "12px",
            borderRadius: "50%",
          }}
          isConnectable={false}
        />
      )}
      <div className="p-1">
        <MessageNodeComponent node={data} />
      </div>
      <div
        className={`absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-b-2xl transition-opacity duration-300 ${
          selected ? "opacity-100" : "opacity-0"
        }`}
      />
      {/* Source handle - only show if node has children */}
      {hasChildren && (
        <Handle
          type="source"
          position={isVertical ? Position.Bottom : Position.Right}
          id={isVertical ? "bottom" : "right"}
          style={{
            background: "linear-gradient(135deg, #6366f1, #8b5cf6)",
            border: "2px solid white",
            width: "12px",
            height: "12px",
          }}
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
  direction = "LR",
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

export const CanvasView: React.FC<CanvasViewProps> = ({
  canvas: externalCanvas,
  showMiniMap = true,
  showControls = true,
  showPanel = true,
}) => {
  return (
    <div className="h-full w-full">
      <ReactFlowProvider>
        <CanvasViewInner
          canvas={externalCanvas}
          showMiniMap={showMiniMap}
          showControls={showControls}
          showPanel={showPanel}
        />
      </ReactFlowProvider>
    </div>
  );
};

const CanvasViewInner: React.FC<CanvasViewProps> = ({
  canvas,
  showMiniMap = true,
  showControls = true,
  showPanel = true,
}) => {
  const reactFlowInstance = useReactFlow();
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  useEffect(() => {
    if (!canvas) {
      setNodes([]);
      setEdges([]);
      return;
    }
    const nodes: Node[] = [];
    const edges: Edge[] = [];

    // Create nodes with parent/children information
    Object.entries(canvas.nodes).forEach(([nodeId, node]) => {
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
          direction: "LR",
        },
        style: { width: 320 },
      });
    });

    // Create edges
    Object.entries(canvas.nodes).forEach(([nodeId, node]) => {
      // check if child node.parent_id is equal to the current nodeId
      node.child_ids.forEach(childId => {
        const is_parent = canvas.nodes[childId]?.parent_id === nodeId;
        edges.push({
          id: `${nodeId}-${childId}`, // from -> to
          source: nodeId,
          target: childId,
          sourceHandle: "bottom",
          targetHandle: "top",
          type: "simplebezier",
          animated: false,
          style: {
            stroke: "#6366f1",
            strokeWidth: 3,
            strokeDasharray: is_parent ? undefined : "5,5",
          },
          markerEnd: {
            type: MarkerType.Arrow,
            width: 15,
            height: 15,
            color: "#6366f1",
          },
        });
      });
    });

    setNodes(nodes);
    setEdges(edges);
  }, [canvas, setNodes, setEdges]);

  // Separate effect to trigger re-layout after nodes are set
  useEffect(() => {
    if (nodes.length > 0 && canvas) {
      // Use setTimeout to ensure nodes are rendered before layout
      const timeoutId = setTimeout(() => {
        // Get current direction from the first node, default to LR
        const currentDirection = nodes[0]?.data?.direction || "LR";
        const { nodes: layoutedNodes, edges: layoutedEdges } =
          getLayoutedElements(nodes, edges, currentDirection, canvas.nodes);

        setNodes([...layoutedNodes]);
        setEdges([...layoutedEdges]);

        // Center the view on the root node
        // find the root nodes from data.nodes
        // a root node is one that has no parent_id
        const root_ids = Object.values(canvas.nodes)
          .filter(node => node.parent_id == null)
          .map(node => node.id);
        const rootNode = layoutedNodes.find(node => node.id === root_ids[0]);
        if (rootNode) {
          const x = rootNode.position.x + (rootNode.width || 320) / 2;
          const y = rootNode.position.y + (rootNode.height || 150) / 2;
          reactFlowInstance.setCenter(x, y, {
            zoom: reactFlowInstance.getZoom(),
            duration: 800,
          });
        }
      }, 100);

      return () => clearTimeout(timeoutId);
    }
  }, [nodes.length, canvas]); // Only trigger when nodes.length changes and we have data

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
            nodeLeft + (selectedNode.width || 320) * viewport.zoom;
          const nodeBottom =
            nodeTop + (selectedNode.height || 150) * viewport.zoom;

          // Check if any part of the node is outside the viewport
          const isOutsideViewport =
            nodeLeft < 0 ||
            nodeTop < 0 ||
            nodeRight > containerWidth ||
            nodeBottom > containerHeight;

          if (isOutsideViewport) {
            const x = selectedNode.position.x + (selectedNode.width || 320) / 2;
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

      const currentX = currentNode.position.x + (currentNode.width || 320) / 2;
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
            const nodeX = n.position.x + (n.width || 320) / 2;
            return nodeX < currentX;
          });
          break;
        case "right":
          candidates = candidates.filter(n => {
            const nodeX = n.position.x + (n.width || 320) / 2;
            return nodeX > currentX;
          });
          break;
      }

      if (candidates.length === 0) return null;

      // Find the closest candidate
      let closest = candidates[0];
      let minDistance = Infinity;

      candidates.forEach(candidate => {
        const candidateX = candidate.position.x + (candidate.width || 320) / 2;
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
      if (!canvas) return;

      // Update nodes with new direction information
      const updatedNodes = nodes.map(node => ({
        ...node,
        data: {
          ...node.data,
          direction,
        },
      }));

      const { nodes: layoutedNodes, edges: layoutedEdges } =
        getLayoutedElements(updatedNodes, edges, direction, canvas.nodes);

      setNodes([...layoutedNodes]);
      setEdges([...layoutedEdges]);
    },
    [nodes, edges, setNodes, setEdges, canvas]
  );

  const onReLayout = useCallback(() => {
    // Get current direction from the first node, default to LR
    const currentDirection = nodes[0]?.data?.direction || "LR";
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
      className="bg-gradient-to-br from-slate-50 to-indigo-50 dark:from-gray-900 dark:to-gray-800"
      defaultEdgeOptions={{
        type: "simplebezier",
        animated: false,
        style: { strokeWidth: 3, stroke: "#6366f1" },
        markerEnd: { type: MarkerType.ArrowClosed, color: "#6366f1" },
      }}
      deleteKeyCode={["Backspace", "Delete"]}
      multiSelectionKeyCode={["Meta", "Ctrl"]}
      tabIndex={0}
      style={{ outline: "none" }}
    >
      <svg
        style={{ position: "absolute", top: 0, left: 0, width: 0, height: 0 }}
      >
        <defs>
          <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#6366f1" />
            <stop offset="100%" stopColor="#8b5cf6" />
          </linearGradient>
        </defs>
      </svg>
      {showControls && (
        <Controls className="bg-white dark:bg-gray-800 !border-gray-200 dark:!border-gray-600 !shadow-lg !rounded-xl [&>button]:!bg-white dark:[&>button]:!bg-gray-700 [&>button]:!border-gray-200 dark:[&>button]:!border-gray-600 [&>button]:!rounded-lg [&>button]:hover:!bg-gray-50 dark:[&>button]:hover:!bg-gray-700 [&>button]:!transition-colors [&>button]:!text-gray-700 dark:[&>button]:!text-gray-300" />
      )}
      {showMiniMap && (
        <MiniMap
          pannable
          zoomable
          nodeColor="#6366f1"
          maskColor="rgba(0, 0, 0, 0.05)"
          className="!bg-white dark:!bg-gray-700 !border-gray-200 dark:!border-gray-600 !shadow-lg !rounded-xl !overflow-hidden"
          style={{ backgroundColor: "rgba(255, 255, 255, 0.95)" }}
        />
      )}
      {showPanel && (
        <Panel
          position="top-left"
          className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-100 dark:border-gray-700 p-4 space-y-3 backdrop-blur-sm bg-white/95 dark:bg-gray-800/95"
        >
          <div className="flex items-center gap-3">
            <div className="w-3 h-3 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full"></div>
            <div className="font-semibold text-gray-900 dark:text-gray-100 text-lg">
              {canvas?.title || "Canvas"}
            </div>
          </div>
          <div className="text-gray-600 dark:text-gray-400 text-sm">
            {canvas ? Object.keys(canvas.nodes).length : 0} messages
          </div>
          <div className="text-xs text-gray-500 dark:text-gray-400 py-2 px-3 bg-gradient-to-r from-indigo-50 to-purple-50 dark:from-indigo-900/20 dark:to-purple-900/20 rounded-xl border border-indigo-100 dark:border-indigo-800">
            💡 Use ↑↓←→ arrow keys to navigate between nodes
          </div>
          <div className="space-y-2">
            <div className="text-xs font-medium text-gray-700 dark:text-gray-300 mb-2">
              Layout Options
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => onLayout("TB")}
                className="group relative overflow-hidden px-3 py-2 text-xs bg-gradient-to-r from-indigo-500 to-purple-500 text-white font-medium rounded-xl shadow-sm hover:shadow-md transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-1 transition-all duration-200"
              >
                <span className="relative z-10 flex items-center">
                  <svg
                    className="w-3 h-3 mr-1"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M19 14l-7 7m0 0l-7-7m7 7V3"
                    />
                  </svg>
                  Vertical
                </span>
                <div className="absolute inset-0 bg-gradient-to-r from-indigo-600 to-purple-600 opacity-0 group-hover:opacity-100 transition-opacity duration-200" />
              </button>
              <button
                onClick={() => onLayout("LR")}
                className="group relative overflow-hidden px-3 py-2 text-xs bg-gradient-to-r from-indigo-500 to-purple-500 text-white font-medium rounded-xl shadow-sm hover:shadow-md transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-1 transition-all duration-200"
              >
                <span className="relative z-10 flex items-center">
                  <svg
                    className="w-3 h-3 mr-1"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M14 5l7 7m0 0l-7 7m7-7H3"
                    />
                  </svg>
                  Horizontal
                </span>
                <div className="absolute inset-0 bg-gradient-to-r from-indigo-600 to-purple-600 opacity-0 group-hover:opacity-100 transition-opacity duration-200" />
              </button>
            </div>
            <button
              onClick={onReLayout}
              className="w-full group relative overflow-hidden px-3 py-2 text-xs bg-gradient-to-r from-emerald-500 to-teal-500 text-white font-medium rounded-xl shadow-sm hover:shadow-md transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:ring-offset-1 transition-all duration-200"
            >
              <span className="relative z-10 flex items-center justify-center">
                <svg
                  className="w-3 h-3 mr-1"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                  />
                </svg>
                Re-layout
              </span>
              <div className="absolute inset-0 bg-gradient-to-r from-emerald-600 to-teal-600 opacity-0 group-hover:opacity-100 transition-opacity duration-200" />
            </button>
          </div>
        </Panel>
      )}
    </ReactFlow>
  );
};
