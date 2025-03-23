import Image from "next/image";

interface ProductImageDetail {
  source: string;
  alt?: string;
}

interface ProductImageProps {
  onClickEventHandler: () => void;
  image: ProductImageDetail;
}

const ProductImage: React.FC<ProductImageProps> = ({
  onClickEventHandler,
  image,
}) => {
  return (
    <Image
      key={image.source}
      className="mask w-16 border-2 p-0.5 border-gray-300 rounded-lg hover:cursor-pointer"
      src={image.source}
      width={200}
      height={200}
      alt={image.alt ? image.alt : ""}
      onClick={onClickEventHandler}
    />
  );
};

export default ProductImage;
