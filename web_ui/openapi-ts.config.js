export default {
  input: "../schemas/openapi.json",
  output: "src/client",
  formatters: ["prettier"],
  typescript: {
    format: true,
  },
};
