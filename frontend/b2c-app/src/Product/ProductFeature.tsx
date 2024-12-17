interface ProductFeatureProps {
  name: string;
  value: string;
}

const ProductFeature: React.FC<ProductFeatureProps> = ({ name, value }) => {
  return (
    <>
      <div className="card bg-base-200 shadow-md min-h-12 max-h-20 overflow-hidden">
        <div className="card-body flex p-3 text-sm items-center">
          <h2>{name}</h2>
          <p className="font-semibold">{value}</p>
        </div>
      </div>
    </>
  );
};

export default ProductFeature;
