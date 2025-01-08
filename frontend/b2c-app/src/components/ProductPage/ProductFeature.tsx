interface ProductFeatureProps {
  name: string;
  value: string;
}

const ProductFeature: React.FC<ProductFeatureProps> = ({ name, value }) => {
  return (
    // text shouldn't be longer than about 23 letters, otherwise the text will be overflowed.
    <>
      <div className="card bg-base-200 shadow-md min-w-[128px]">
        <div className="card-body flex p-1 text-xs items-center">
          <h2>{name}</h2>
          <p className="font-semibold">{value}</p>
        </div>
      </div>
    </>
  );
};

export default ProductFeature;
