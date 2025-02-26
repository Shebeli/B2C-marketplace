import Image from "next/image";

interface ProductCardProps {
  id: number;
  name: string;
  image: string;
  price: number;
  sellerName: string;
  sellerPic: string;
}

export default function ProductCard({
  id,
  name,
  image,
  price,
  sellerName,
  sellerPic,
}: ProductCardProps) {
  return (
    <div key={id} className="card bg-base-100 shadow-lg">
      <figure className="mx-8 min-h-52 min-w-52">
        <Image
          src={image}
          width={300}
          height={300}
          alt={name}
          className="rounded-lg"
        />
      </figure>
      <div className="card-body">
        <h2 className="card-title text-sm">{name}</h2>
        <div className="flex items-center">
          <div className="avatar">
            <div className="w-7 rounded-full">
              <Image src={sellerPic} alt={sellerName} width={30} height={30} />
            </div>
          </div>
          <span className="text-sm mr-1.5">{sellerName}</span>
        </div>

        <p className=" text-left text-">{price.toLocaleString()} تومان</p>
        <div className="card-actions justify-end">
          <button className="btn btn-primary btn-sm ">مشاهده محصول</button>
        </div>
      </div>
    </div>
  );
}
