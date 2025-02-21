import Image from "next/image";

interface ProductImageDetail {
    source: string;
    alt?: string;
  }
  
  interface ProductImageProps {
    setOpenedImage: React.Dispatch<React.SetStateAction<string | null>>;
    images: Array<ProductImageDetail>;
  }
  
  const ProductImage: React.FC<ProductImageProps> = ({
    setOpenedImage,
    images,
  }) => {
    return (
      <div className="flex self-start pb-1 gap-3 scrollbar overflow-x-auto scrollbar-thumb-rounded-full scrollbar-track-rounded-full scrollbar-thumb-slate-700 scrollbar-track-slate-300">
        {images.map((image) => (
          <Image
            key={image.source}
            className="mask w-16 border-2 p-0.5 border-gray-300 rounded-lg hover:cursor-pointer"
            src={image.source}
            width={200}
            height={200}
            alt={image.alt ? image.alt : ""}
            onClick={() => setOpenedImage(image.source)}
          />
        ))}
      </div>
    );
  };
  
  export default ProductImage;
  