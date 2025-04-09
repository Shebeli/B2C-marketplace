"use client";

import Image from "next/image";
import { FaShieldHalved, FaStar, FaStore } from "react-icons/fa6";
import ProductColorVariant from "./product-color-variant";
import ProductFeatures from "./product-feature";
import ProductImage from "./product-image";
import ProductImageModal from "./product-image-modal";
import { FaCheck } from "react-icons/fa6";
import { ProductDetailUI } from "@/app/lib/types/ui/product-detail/productDetailsUI";
import { useState } from "react";
import { ProductVariantUI } from "@/app/lib/types/ui/product-detail/productDetailsUI";

interface ProductMainProps {
  product: ProductDetailUI;
}

export default function ProductMain({ product }: ProductMainProps) {
  const [selectedVariant, setSelectedVariant] = useState<ProductVariantUI>(
    product.variants[0]
  );

  // clicked product image modal
  const [openedImageSrc, setOpenedImageSrc] = useState<string | null>(null);

  return (
    <div>
      <ProductImageModal
        openedImageSrc={openedImageSrc}
        setOpenedImageSrc={setOpenedImageSrc}
      />
      <div className="justify-items m-2 w-full">
        <div className="flex flex-col lg:flex-row">
          <div className="card grid basis-3/6 place-items-center lg:ml-2 mb-2 ">
            <Image
              className="mask lg:w-9/12 w-3/6 rounded-2xl pb-4"
              src="/sample_images/product-main-image.webp"
              alt="Laptop"
              width={1000}
              height={1000}
            />
            <div className="flex self-start pb-1 gap-3 scrollbar overflow-x-auto scrollbar-thumb-rounded-full scrollbar-track-rounded-full scrollbar-thumb-slate-700 scrollbar-track-slate-300">
              {product.variants.flatMap((variant) =>
                variant.images.map((image, index) => (
                  <ProductImage
                    key={variant.id}
                    imageSource={image}
                    imageAlt={`${product.name} ${variant.name} ${index}`}
                    onClickEventHandler={() => setOpenedImageSrc(image)}
                  />
                ))
              )}
            </div>
          </div>
          <div>
            <div className="card bg-base-200 rounded-box min-h-16 max-h-48 basis-2/3 p-3 lg:mx-0">
              <div className="breadcrumbs text-sm pt-2 pb-1">
                <ul>
                  <li>
                    <a>{product.breadCrumb.mainCategory}</a>
                  </li>
                  <li>
                    <a>{product.breadCrumb.category}</a>
                  </li>
                  <li>
                    <a>{product.breadCrumb.subCategory}</a>
                  </li>
                </ul>
              </div>
              <h1 className="text-lg leading-8 font-medium">{product.name}</h1>
            </div>
            <div className="grid grid-rows-[auto_1fr] lg:grid-cols-[8fr_5fr] grid-cols-[1fr_2fr] my-3 wrap gap-4">
              <div className="lg mx-4">
                <div className="flex gap-1">
                  <FaStar className=" text-yellow-300" />
                  <p className="font-light text-sm">
                    {product.ratingAvg} امتیاز ( از {product.ratingCount}{" "}
                    خریدار)
                  </p>
                </div>
                <ProductColorVariant
                  variants={product.variants}
                  selectedVariant={selectedVariant}
                  setSelectedVariant={setSelectedVariant}
                />
              </div>
              <div className="card h-fit lg:w-full w-8/12 min-w-64 max-w-96 shadow-xl bg-base-200 mr-auto font-medium text-sm col-span-1 row-span-2 ">
                <div className="card-body p-5 flex flex-col gap-3">
                  <h2 className="card-title">فروشنده</h2>
                  <div className="flex gap-2 border-b-[1px] pb-2 border-base-300">
                    <FaStore className="text-xl text-orange-400" />
                    <p>{product.owner.storeName}</p>
                  </div>
                  <div className="flex justify-between my-1 font-medium ">
                    <span>قیمت</span>
                    <span>{selectedVariant.price} تومان</span>
                  </div>
                  <div className="flex gap-2 text-xl border-b-[2px] pb-2 border-base-300">
                    <FaShieldHalved className="text-blue-400" />
                    <p className="text-sm"> گارانتی 24 ماهه آوا</p>
                  </div>
                  <div className="flex gap-2 ">
                    <FaCheck className=" text-green-600 text-xl" />
                    <p>شامل ضمانت 7 روزه</p>
                  </div>
                  <div className="card-actions justify-center">
                    <button className="btn btn-primary mt-2 w-full">
                      افزودن به سبد خرید
                    </button>
                  </div>
                </div>
              </div>
              <ProductFeatures productFeatures={product.productFeatures} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
