import {
  TechnicalDetail,
  ProductOwner,
  Breadcrumb,
} from "../../api/responses/product-detail/productResponse";

export interface ProductFeatureUI {
  attribute: string;
  value: string;
}

export interface ProductVariantUI {
  id: number;
  name: string;
  price: number;
  images: string[];
  colorName: string | null; // name to be displayed
  colorValue: string | null; // hex code
}

export interface ProductDetailUI {
  id: number;
  technicalDetails: TechnicalDetail[];
  productFeatures: ProductFeatureUI[];
  variants: ProductVariantUI[];
  owner: ProductOwner;
  ratingAvg: number;
  ratingCount: number;
  name: string;
  description: string;
  breadCrumb: Breadcrumb;
}
