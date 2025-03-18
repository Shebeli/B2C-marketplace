import Image from "next/image";
import MainLayout from "./main/layout";
import HomeModal from "./ui/home-modal";
import { DEFAULT_PRODUCT_IMAGE_URL } from "./lib/constants/assets";

// This component is exceptionally wrapped by MainLayout
export default function Home() {
  return (
    <MainLayout>
      <HomeModal />
      <div className="p-4 max-w-(--breakpoint-2xl)">
        <div className="hero ">
          <div className="hero-content flex-col lg:flex-row-reverse lg:gap-32 gap-12 py-12">
            <Image
              src={"/home/home-banner.webp"}
              width={750}
              height={500}
              alt="Pigikala Home Banner"
              className="rounded-full shadow-2xl lg:size-3/12 sm:size-4/12 size-7/12 lg:my-4"
            />
            <div>
              <h1 className="text-5xl font-bold">بهترین ها را بخرید!</h1>
              <p className="pt-8 text-2xl">
                بهترین کالا های مورد پسند خودتان را از فروشنده مد نظرتان را
                انتخاب کرده و سفارش دهید!
              </p>
            </div>
          </div>
        </div>

        {/* Categories Section */}
        <div className="mt-8">
          <h2 className="text-3xl font-bold text-center">خرید از دسته بندی</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
            <div className="card bg-base-100 shadow-lg">
              <figure>
                <Image
                  src="/home/fashion-category.jpg"
                  width={750}
                  height={500}
                  alt="Pigikala Home Fashion Banner"
                  className="rounded-lg lg:w-full w-3/4"
                />
              </figure>
              <div className="card-body">
                <h2 className="card-title">لباس و مد</h2>
                <p>بروز ترین و شیک ترین لباس ها</p>
                <div className="card-actions justify-end">
                  <button className="btn btn-outline btn-primary">
                    دیدن محصولات
                  </button>
                </div>
              </div>
            </div>

            <div className="card bg-base-100 shadow-lg">
              <figure>
                <Image
                  src="/home/electronics-category.jpg"
                  width={750}
                  height={500}
                  alt="Pigikala Home Electronic Banner"
                  className="rounded-lg lg:w-full w-3/4"
                />
              </figure>
              <div className="card-body">
                <h2 className="card-title">الکترونیکی</h2>
                <p>جدید ترین و مدرن ترین وسایل الکترونیکی و گجت ها</p>
                <div className="card-actions justify-end">
                  <button className="btn btn-outline btn-primary">
                    دیدن محصولات
                  </button>
                </div>
              </div>
            </div>

            <div className="card bg-base-100 shadow-lg">
              <figure>
                <Image
                  src="/home/home-furniture-category.jpg"
                  width={750}
                  height={500}
                  alt="Pigikala Home Goods Banner"
                  className="rounded-lg lg:w-full w-3/4"
                />
              </figure>
              <div className="card-body">
                <h2 className="card-title">وسایل خانگی</h2>
                <p>جدید ترین و بروزترین وسایل خانگی</p>
                <div className="card-actions justify-end">
                  <button className="btn btn-outline btn-primary">
                    مشاهده محصولات
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Featured Products Section */}
        <div className="mt-12">
          <h2 className="text-3xl font-bold text-center">محصولات ویژه</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mt-6">
            {Array(4)
              .fill(null)
              .map((_, index) => (
                <div key={index} className="card bg-base-100 shadow-lg">
                  <figure>
                    <Image
                      src={DEFAULT_PRODUCT_IMAGE_URL}
                      width={500}
                      height={300}
                      alt={`Product ${index + 1}`}
                      className="rounded-lg"
                    />
                  </figure>
                  <div className="card-body">
                    <h2 className="card-title">Product {index + 1}</h2>
                    <p>500,000 هزار تومان</p>
                    <div className="card-actions justify-end">
                      <button className="btn btn-primary">مشاهده محصول</button>
                    </div>
                  </div>
                </div>
              ))}
          </div>
        </div>
      </div>
    </MainLayout>
  );
}
