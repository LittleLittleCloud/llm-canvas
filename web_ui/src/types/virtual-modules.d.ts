declare module "virtual:example-sources" {
  export const exampleSourceCode: Record<string, string>;
  export function getSourceCodeForCanvas(
    canvasTitle: string
  ): string | undefined;
  export function getGithubLinkForCanvas(
    canvasTitle: string
  ): string | undefined;
}
