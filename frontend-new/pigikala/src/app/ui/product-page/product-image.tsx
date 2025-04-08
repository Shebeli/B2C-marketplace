import Image from "next/image";
import { ProductImageDetail } from "@/app/lib/types/ui/generalTypes";

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
      width={200}
      height={200}
      alt={imageAlt}
      onClick={onClickEventHandler}
    />
  );
};

export default ProductImage;
