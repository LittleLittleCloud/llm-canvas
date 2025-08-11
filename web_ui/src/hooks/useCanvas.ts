import { useCallback } from "react";
import { useCanvasStore } from "../store/canvasStore";
import { MessageNode } from "../types";

/**
 * Custom hook for canvas operations and utilities
 */
export const useCanvas = () => {
  const canvas = useCanvasStore(state => state.canvas);
  const actions = useCanvasStore(state => ({
    setCanvas: state.setCanvas,
    setLoading: state.setLoading,
    setError: state.setError,
    addMessage: state.addMessage,
  }));

  // Helper to add a user message
  const addUserMessage = useCallback(
    (content: string, parentId?: string) => {
      return actions.addMessage(content, "user", parentId);
    },
    [actions]
  );

  // Helper to add an assistant message
  const addAssistantMessage = useCallback(
    (content: string, parentId?: string) => {
      return actions.addMessage(content, "assistant", parentId);
    },
    [actions]
  );

  // Get conversation thread from a node to root
  const getConversationThread = useCallback(
    (nodeId: string): MessageNode[] => {
      if (!canvas) return [];

      const thread: MessageNode[] = [];
      let currentId: string | null = nodeId;

      while (currentId && canvas.nodes[currentId]) {
        const node: MessageNode = canvas.nodes[currentId];
        thread.unshift(node);
        currentId = node.parent_id || null;
      }

      return thread;
    },
    [canvas]
  );

  // Get all leaf nodes (nodes with no children)
  const getLeafNodes = useCallback((): MessageNode[] => {
    if (!canvas) return [];

    return Object.values(canvas.nodes).filter(
      node => node.child_ids.length === 0
    );
  }, [canvas]);

  // Get conversation branches from a specific node
  const getBranches = useCallback(
    (nodeId: string): MessageNode[][] => {
      if (!canvas) return [];

      const branches: MessageNode[][] = [];
      const node = canvas.nodes[nodeId];

      if (!node) return [];

      // If this is a leaf node, return the thread
      if (node.child_ids.length === 0) {
        return [getConversationThread(nodeId)];
      }

      // Otherwise, get branches from each child
      node.child_ids.forEach(childId => {
        const childBranches = getBranches(childId);
        branches.push(...childBranches);
      });

      return branches;
    },
    [canvas, getConversationThread]
  );

  // Get statistics about the canvas
  const getStats = useCallback(() => {
    if (!canvas) {
      return {
        totalNodes: 0,
        userMessages: 0,
        assistantMessages: 0,
        branches: 0,
        maxDepth: 0,
      };
    }

    const nodes = Object.values(canvas.nodes);
    const userMessages = nodes.filter(n => n.message.role === "user").length;
    const assistantMessages = nodes.filter(
      n => n.message.role === "assistant"
    ).length;
    const leafNodes = getLeafNodes();

    // Calculate max depth
    let maxDepth = 0;
    leafNodes.forEach(leaf => {
      const thread = getConversationThread(leaf.id);
      maxDepth = Math.max(maxDepth, thread.length);
    });

    return {
      totalNodes: nodes.length,
      userMessages,
      assistantMessages,
      branches: leafNodes.length,
      maxDepth,
    };
  }, [canvas, getLeafNodes, getConversationThread]);

  // Check if a node has siblings
  const hasSiblings = useCallback(
    (nodeId: string): boolean => {
      if (!canvas) return false;

      const node = canvas.nodes[nodeId];
      if (!node || !node.parent_id) return false;

      const parent = canvas.nodes[node.parent_id];
      return parent ? parent.child_ids.length > 1 : false;
    },
    [canvas]
  );

  return {
    // State
    canvas,

    // Basic actions
    ...actions,

    // Convenience methods
    addUserMessage,
    addAssistantMessage,

    // Utilities
    getConversationThread,
    getLeafNodes,
    getBranches,
    getStats,
    hasSiblings,
  };
};

export default useCanvas;
