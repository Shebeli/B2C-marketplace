import React from "react";

interface Detail {
  name: string;
  value: string;
}

interface Props {
  details: Array<Detail>;
}

const ProductDetail: React.FC<Props> = ({ details }) => {
  return (
    <section>
      <ul className="grid md:grid-cols-2">
        {details.map((detail, index) => (
          <li key={index} className="flex gap-8 border-b-2 border-base-300 py-3">
            <p className="font-semibold">{detail.name}</p>
            <p className="">{detail.value}</p>
          </li>
        ))}
      </ul>
    </section>
  );
};

export default ProductDetail;
