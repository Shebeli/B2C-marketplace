interface Color {
  name: string;
  code: string; // hex code
  price: string; // 3,000,222,000
}

interface ProductColorProps {
  colors: Array<Color>;
  selectedColor: string;
  setSelectedColor: React.Dispatch<React.SetStateAction<string>>;
}

const ProductColor: React.FC<ProductColorProps> = ({
  colors,
  selectedColor,
  setSelectedColor,
}) => {
  return (
    <div>
      <p>رنگ انتخاب شده: {selectedColor}</p>
      <div className="flex my-2 gap-2">
        {colors.map((color) => (
          <button
            key={color.name}
            className={`w-9 h-9 rounded-full ${
              selectedColor === color.name
                ? "ring-4 border-[3.5px] ring-cyan-500"
                : ""
            }`}
            style={{ backgroundColor: `#${color.code}` }}
            onClick={() => setSelectedColor(color.name)}
          ></button>
        ))}
      </div>
    </div>
  );
};

export default ProductColor;
