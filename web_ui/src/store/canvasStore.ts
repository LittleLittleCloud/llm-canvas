import { create } from "zustand";
import { devtools } from "zustand/middleware";
import { config } from "../config";
import { CanvasData, Message, MessageNode } from "../types";

export interface CanvasState {
  // Canvas data
  canvas: CanvasData | null;
  isLoading: boolean;
  error: string | null;

  // Actions
  setCanvas: (canvas: CanvasData) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;

  // Canvas operations
  addMessage: (
    content: string | Message,
    role: "user" | "assistant" | "system",
    parentId?: string | null,
    meta?: Record<string, any>
  ) => MessageNode;

  updateMessage: (nodeId: string, updates: Partial<MessageNode>) => void;
  removeMessage: (nodeId: string) => void;

  // Data fetching
  fetchCanvas: () => Promise<void>;
  refreshCanvas: () => Promise<void>;

  // Utilities
  getNode: (nodeId: string) => MessageNode | null;
  getChildren: (nodeId: string) => MessageNode[];
  getRootNodes: () => MessageNode[];
  clear: () => void;
}

const generateId = () => crypto.randomUUID();

const normalizeContent = (
  content: string | Message,
  role?: "user" | "assistant" | "system"
): Message => {
  if (typeof content === "string") {
    if (role) {
      return { content, role };
    }

    throw new Error("Content must be a string or an array of messages");
  }
  return content;
};

// API base URL configuration
const getApiBaseUrl = () => {
  return config.api.baseUrl;
};

const apiCall = async (endpoint: string, options?: RequestInit) => {
  const baseUrl = getApiBaseUrl();
  const url = `${baseUrl}${endpoint}`;

  const response = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
    method: "GET",
  });

  if (!response.ok) {
    throw new Error(
      `API call failed: ${response.status} ${response.statusText}`
    );
  }

  return response;
};

export const useCanvasStore = create<CanvasState>()(
  devtools(
    (set, get) => ({
      // Initial state
      canvas: null,
      isLoading: false,
      error: null,

      // Basic setters
      setCanvas: canvas => set({ canvas, error: null }),
      setLoading: isLoading => set({ isLoading }),
      setError: error => set({ error }),

      // Canvas operations
      addMessage: (content, role, parentId = null, meta = {}) => {
        const state = get();
        if (!state.canvas) {
          throw new Error("Canvas not initialized");
        }

        const nodeId = generateId();
        const newNode: MessageNode = {
          id: nodeId,
          content: normalizeContent(content, role),
          parent_id: parentId,
          child_ids: [],
          meta: {
            timestamp: Date.now(),
            ...meta,
          },
        };

        const updatedNodes = { ...state.canvas.nodes };
        updatedNodes[nodeId] = newNode;

        // Update parent's child_ids if this has a parent
        if (parentId && updatedNodes[parentId]) {
          updatedNodes[parentId] = {
            ...updatedNodes[parentId],
            child_ids: [...updatedNodes[parentId].child_ids, nodeId],
          };
        }

        // Update root_ids if this is a root node
        const updatedRootIds = parentId
          ? state.canvas.root_ids
          : [...state.canvas.root_ids, nodeId];

        set({
          canvas: {
            ...state.canvas,
            nodes: updatedNodes,
            root_ids: updatedRootIds,
          },
        });

        return newNode;
      },

      updateMessage: (nodeId, updates) => {
        const state = get();
        if (!state.canvas || !state.canvas.nodes[nodeId]) {
          return;
        }

        const updatedNodes = { ...state.canvas.nodes };
        updatedNodes[nodeId] = {
          ...updatedNodes[nodeId],
          ...updates,
        };

        set({
          canvas: {
            ...state.canvas,
            nodes: updatedNodes,
          },
        });
      },

      removeMessage: nodeId => {
        const state = get();
        if (!state.canvas || !state.canvas.nodes[nodeId]) {
          return;
        }

        const nodeToRemove = state.canvas.nodes[nodeId];
        const updatedNodes = { ...state.canvas.nodes };

        // Remove from parent's child_ids
        if (nodeToRemove.parent_id && updatedNodes[nodeToRemove.parent_id]) {
          updatedNodes[nodeToRemove.parent_id] = {
            ...updatedNodes[nodeToRemove.parent_id],
            child_ids: updatedNodes[nodeToRemove.parent_id].child_ids.filter(
              id => id !== nodeId
            ),
          };
        }

        // Remove from root_ids if it's a root
        const updatedRootIds = state.canvas.root_ids.filter(
          id => id !== nodeId
        );

        // Recursively remove all children
        const removeNodeAndChildren = (id: string) => {
          const node = updatedNodes[id];
          if (node) {
            node.child_ids.forEach(removeNodeAndChildren);
            delete updatedNodes[id];
          }
        };

        removeNodeAndChildren(nodeId);

        set({
          canvas: {
            ...state.canvas,
            nodes: updatedNodes,
            root_ids: updatedRootIds,
          },
        });
      },

      // Data fetching
      fetchCanvas: async () => {
        set({ isLoading: true, error: null });
        try {
          const response = await apiCall("/canvas");
          const canvas = await response.json();
          set({ canvas, isLoading: false });
        } catch (error) {
          set({
            error:
              error instanceof Error ? error.message : "Failed to fetch canvas",
            isLoading: false,
          });
        }
      },

      refreshCanvas: async () => {
        const state = get();
        if (state.canvas) {
          await state.fetchCanvas();
        }
      },

      // Utilities
      getNode: nodeId => {
        const state = get();
        return state.canvas?.nodes[nodeId] || null;
      },

      getChildren: nodeId => {
        const state = get();
        if (!state.canvas) return [];

        const node = state.canvas.nodes[nodeId];
        if (!node) return [];

        return node.child_ids
          .map(id => state.canvas!.nodes[id])
          .filter(Boolean);
      },

      getRootNodes: () => {
        const state = get();
        if (!state.canvas) return [];

        return state.canvas.root_ids
          .map(id => state.canvas!.nodes[id])
          .filter(Boolean);
      },

      clear: () => set({ canvas: null, isLoading: false, error: null }),
    }),
    {
      name: "canvas-store",
    }
  )
);
