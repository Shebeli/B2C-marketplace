import Image from "next/image";

interface ProductImageProps {
  onClickEventHandler: () => void;
  imageSource: string;
  imageAlt: string;
}

const ProductImage: React.FC<ProductImageProps> = ({
  onClickEventHandler,
  imageSource,
  imageAlt,
}) => {
  return (
    <Image
      className="mask w-16 border-2 p-0.5 border-gray-300 rounded-lg hover:cursor-pointer"
      src={imageSource}
      width={100}
      height={100}
      alt={imageAlt}
      onClick={onClickEventHandler}
    />
  );
};

export default ProductImage;
