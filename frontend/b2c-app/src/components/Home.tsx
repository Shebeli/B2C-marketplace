import React from "react";

const Home: React.FC = () => {
  return (
    <div className="p-4">
      {/* Hero Section */}
      <div className="hero bg-base-200 rounded-lg">
        <div className="hero-content flex-col lg:flex-row-reverse">
          <img
            src="https://via.placeholder.com/500"
            alt="E-commerce Banner"
            className="rounded-lg shadow-2xl max-w-sm lg:max-w-lg"
          />
          <div>
            <h1 className="text-5xl font-bold">Shop the Latest Trends!</h1>
            <p className="py-6">
              Discover our newest collection of products at unbeatable prices.
              Whether you're looking for fashion, electronics, or home goods,
              we've got something for everyone.
            </p>
            <button className="btn btn-primary">Shop Now</button>
          </div>
        </div>
      </div>

      {/* Categories Section */}
      <div className="mt-8">
        <h2 className="text-3xl font-bold text-center">Shop by Category</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
          <div className="card bg-base-100 shadow-lg">
            <figure>
              <img
                src="https://via.placeholder.com/300"
                alt="Fashion"
                className="rounded-lg"
              />
            </figure>
            <div className="card-body">
              <h2 className="card-title">Fashion</h2>
              <p>Explore our trendy clothing and accessories.</p>
              <div className="card-actions justify-end">
                <button className="btn btn-outline btn-primary">
                  Shop Now
                </button>
              </div>
            </div>
          </div>

          <div className="card bg-base-100 shadow-lg">
            <figure>
              <img
                src="https://via.placeholder.com/300"
                alt="Electronics"
                className="rounded-lg"
              />
            </figure>
            <div className="card-body">
              <h2 className="card-title">Electronics</h2>
              <p>Find the latest gadgets and devices.</p>
              <div className="card-actions justify-end">
                <button className="btn btn-outline btn-primary">
                  Shop Now
                </button>
              </div>
            </div>
          </div>

          <div className="card bg-base-100 shadow-lg">
            <figure>
              <img
                src="https://via.placeholder.com/300"
                alt="Home Goods"
                className="rounded-lg"
              />
            </figure>
            <div className="card-body">
              <h2 className="card-title">Home Goods</h2>
              <p>Upgrade your home with our premium products.</p>
              <div className="card-actions justify-end">
                <button className="btn btn-outline btn-primary">
                  Shop Now
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Featured Products Section */}
      <div className="mt-12">
        <h2 className="text-3xl font-bold text-center">Featured Products</h2>
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
                  <p>$99.99</p>
                  <div className="card-actions justify-end">
                    <button className="btn btn-primary">Add to Cart</button>
                  </div>
                </div>
              </div>
            ))}
        </div>
      </div>
    </div>
  );
};

export default Home;
