import { z } from "zod";
import { sortOptions } from "../constants/ui/product-list-constants";

const ProductGenericFilterSchema = z
  .object({
    minPrice: z.coerce.number().nonnegative().optional(),
    maxPrice: z.coerce.number().nonnegative().optional(),
    isAvailable: z.coerce.boolean().optional(),
    canDeliverToday: z.coerce.boolean().optional(),
  })
  .refine(
    (data) =>
      !(data.maxPrice !== undefined && data.minPrice !== undefined) ||
      data.maxPrice >= data.minPrice,
    {
      message: "Max price should be higher or equal to min price",
      path: ["min"],
    }
  );

// dynamic filters to be managed later
export const ProductGeneralParamsChema = z.object({
  subCategoryId: z.coerce.number(),
  page: z.coerce.number().int().positive().optional().default(1),
  sort: z.enum(sortOptions).default("created_at"),
  selectedColors: z
    .string()
    .optional()
    .transform((colors) => (colors ? colors.split(",") : [])), // in hex code
});

export const ProductQueryParamsSchema = z.intersection(
  ProductGenericFilterSchema,
  ProductGeneralParamsChema
);
