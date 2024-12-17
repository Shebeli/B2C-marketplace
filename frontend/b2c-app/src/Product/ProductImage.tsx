interface ProductImageDetail {
  source: string;
  alt?: string;
}

interface ProductImageProps {
  images: Array<ProductImageDetail>;
}

const ProductImage: React.FC<ProductImageProps> = ({ images }) => {
  return (
    <div className="flex self-start pb-1 gap-3 scrollbar overflow-x-auto scrollbar-thumb-rounded-full scrollbar-track-rounded-full scrollbar-thumb-slate-700 scrollbar-track-slate-300">
      {images.map((image) => (
        <img
          key={image.source}
          className="mask w-16 border-2 p-0.5 border-gray-300 rounded-lg"
          src={image.source}
          alt={image.alt ? image.alt : ""}
        />
      ))}
    </div>
  );
};

export default ProductImage;
