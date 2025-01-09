import React, { useEffect, useRef } from "react";
import { useState } from "react";

const Home: React.FC = () => {
  const welcomeModalRef = useRef<HTMLDialogElement>(null);

  const [isWelcomeModalOpen, setIsWelcomeModalOpen] = useState(true);

  useEffect(() => {
    if (isWelcomeModalOpen) {
      welcomeModalRef.current?.showModal();
    } else {
      welcomeModalRef.current?.close();
    }
  });
  return (
    <>
      {" "}
      <div>
        {isWelcomeModalOpen && (
          <dialog ref={welcomeModalRef} id="my_modal_3" className="modal">
            <div className="modal-box">
              <form method="dialog">
                <button
                  onClick={() => setIsWelcomeModalOpen(false)}
                  className="btn btn-sm btn-ghost btn-circle absolute right-2 top-2"
                >
                  ✕
                </button>
              </form>
              <h3 className="font-bold text-lg mt-4"> خوش آمدید!</h3>
              <p className="py-4">
                این پروژه نرم افزاری توسط شروین سعیدی برنا طراحی شده است.
              </p>
            </div>
          </dialog>
        )}
      </div>
      <div className="p-4 max-w-screen-2xl">
        <div className="hero bg-gradient-to-r from-base-100 to-sky-200 rounded-lg">
          <div className="hero-content flex-col lg:flex-row-reverse lg:gap-32 gap-12 py-12">
            <img
              src="home/home-banner.webp"
              alt="E-commerce Banner"
              className="rounded-full shadow-2xl lg:size-3/12 size-6/12 lg:my-4"
            />
            <div>
              <h1 className="text-5xl font-bold">بهترین کالا ها را بخرید!</h1>
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
                <img
                  src="home/fashion-category.jpg"
                  alt="Fashion"
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
                <img
                  src="home/electronics-category.jpg"
                  alt="Electronics"
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
                <img
                  src="home/home-furniture-category.jpg"
                  alt="Home Goods"
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
                    <img
                      src="https://via.placeholder.com/300"
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
    </>
  );
};

export default Home;
