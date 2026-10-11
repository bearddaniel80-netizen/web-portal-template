import { get_service_manager, post_service_manager } from "../utils/serviceManager.js";

export function forwardFastapi(endpoint, isGET = true) {
  return async (req, res, next) => {
    try {
      const path =
        typeof endpoint === "function"
          ? endpoint(req)
          : endpoint;

      const result = isGET ? await get_service_manager(path) : post_service_manager(path);

      res
        .status(result.status)
        .json(result.data);

    } catch (error) {
      next(error);
    }
  };
}