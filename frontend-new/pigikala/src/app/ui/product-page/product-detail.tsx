interface TechnicalDetail {
  attribute: string;
  value: string;
}

interface ProductTechnicalDetailProps {
  technicalDetails: TechnicalDetail[];
}

const ProductTechnicalDetails: React.FC<ProductTechnicalDetailProps> = ({
  technicalDetails,
}) => {
  return (
    <section>
      <ul className="grid md:grid-cols-2">
        {technicalDetails.map((detail, index) => (
          <li
            key={index}
            className="flex gap-8 border-b-2 border-base-300 py-3"
          >
            <p className="font-semibold">{detail.attribute}</p>
            <p className="">{detail.value}</p>
          </li>
        ))}
      </ul>
    </section>
  );
};

export default ProductTechnicalDetails;
