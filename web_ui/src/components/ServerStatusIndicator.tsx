import { Loader2, Plug, PlugZap } from "lucide-react";
import React, { useState } from "react";
import { useServerStatus } from "../hooks/useServerStatus";
import { Button } from "./ui/button";

interface ServerStatusIndicatorProps {
  className?: string;
}

export const ServerStatusIndicator: React.FC<ServerStatusIndicatorProps> = ({
  className = "",
}) => {
  const { status, lastChecked, serverType, error, checkStatus } =
    useServerStatus();
  const [showPopout, setShowPopout] = useState(false);

  const getStatusColor = () => {
    switch (status) {
      case "healthy":
        return "text-green-400";
      case "error":
        return "text-red-400";
      case "loading":
        return "text-yellow-400";
      default:
        return "text-gray-400";
    }
  };

  const getHoverStatusColor = () => {
    switch (status) {
      case "healthy":
        return "hover:text-green-300";
      case "error":
        return "hover:text-red-300";
      case "loading":
        return "hover:text-yellow-300";
      default:
        return "hover:text-gray-300";
    }
  };

  const getStatusIcon = () => {
    switch (status) {
      case "healthy":
        return <PlugZap className="w-5 h-5" />; // Connected plug with electricity
      case "error":
        return <Plug className="w-5 h-5" />; // Unplugged/disconnected
      case "loading":
        return <Loader2 className="w-5 h-5 animate-spin" />; // Loading spinner
      default:
        return <Plug className="w-5 h-5" />; // Default plug icon
    }
  };

  const getStatusText = () => {
    switch (status) {
      case "healthy":
        return "Plugged In";
      case "error":
        return "Unplugged";
      case "loading":
        return "Connecting...";
      default:
        return "Unknown";
    }
  };

  const formatLastChecked = (date: Date | null) => {
    if (!date) return "Never";
    return date.toLocaleTimeString();
  };

  return (
    <div className={`relative ${className}`}>
      {/* Connection Status Button */}
      <Button
        onClick={() => setShowPopout(!showPopout)}
        variant="ghost"
        size="icon"
        className={`${getStatusColor()} ${getHoverStatusColor()} hover:bg-white/10 duration-200`}
        title="Click to view server status details"
      >
        {getStatusIcon()}
      </Button>

      {/* Popout Panel */}
      {showPopout && (
        <>
          {/* Backdrop to close popout when clicking outside */}
          <div
            className="fixed inset-0 z-10"
            onClick={() => setShowPopout(false)}
          />

          {/* Popout Content */}
          <div className="absolute right-8 top-10 z-20 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 rounded-lg shadow-lg border border-gray-200 dark:border-gray-600 p-3 min-w-56">
            <div className="space-y-2">
              {/* Header */}
              <div className="flex items-center justify-between">
                <h3 className="font-medium text-sm">Server Status</h3>
                <button
                  onClick={() => setShowPopout(false)}
                  className="text-gray-400 hover:text-gray-600 dark:text-gray-500 dark:hover:text-gray-300 text-sm"
                >
                  ✕
                </button>
              </div>

              {/* Status */}
              <div className="flex items-center space-x-2">
                <div className={`${getStatusColor()}`}>
                  {React.cloneElement(getStatusIcon() as React.ReactElement, {
                    className: "w-4 h-4",
                  })}
                </div>
                <span className="text-sm">{getStatusText()}</span>
              </div>

              {/* Server Type */}
              {serverType && (
                <div className="text-xs text-gray-500 dark:text-gray-400">
                  Type: {serverType === "local" ? "Local" : "Cloud"}
                </div>
              )}

              {/* Last Checked */}
              <div className="text-xs text-gray-500 dark:text-gray-400">
                Last checked: {formatLastChecked(lastChecked)}
              </div>

              {/* Error Message */}
              {error && (
                <div className="text-xs text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/20 p-2 rounded">
                  {error}
                </div>
              )}

              {/* Refresh Button */}
              <Button
                onClick={() => {
                  checkStatus();
                }}
                variant="ghost"
                size="sm"
                className="w-full text-xs"
                disabled={status === "loading"}
              >
                {status === "loading" ? "Checking..." : "Refresh"}
              </Button>
            </div>
          </div>
        </>
      )}
    </div>
  );
};
