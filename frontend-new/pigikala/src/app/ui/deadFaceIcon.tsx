export default function DeadFaceIcon({
  width,
  height,
}: {
  width: number;
  height: number;
}) {
  return (
    <svg
      width={`${width}px`}
      height={`${height}px`}
      viewBox="0 0 512 512"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        fill="var(--ci-primary-color, #000000)"
        d="M256,16C123.452,16,16,123.452,16,256S123.452,496,256,496,496,388.548,496,256,388.548,16,256,16ZM403.078,403.078a207.253,207.253,0,1,1,44.589-66.125A207.332,207.332,0,0,1,403.078,403.078Z"
        className="ci-primary"
      />
      <rect
        width="176"
        height="32"
        x="168"
        y="320"
        fill="var(--ci-primary-color, #000000)"
        className="ci-primary"
      />
      <polygon
        fill="var(--ci-primary-color, #000000)"
        points="210.63 228.042 186.588 206.671 207.958 182.63 184.042 161.37 162.671 185.412 138.63 164.042 117.37 187.958 141.412 209.329 120.042 233.37 143.958 254.63 165.329 230.588 189.37 251.958 210.63 228.042"
        className="ci-primary"
      />
      <polygon
        fill="var(--ci-primary-color, #000000)"
        points="383.958 182.63 360.042 161.37 338.671 185.412 314.63 164.042 293.37 187.958 317.412 209.329 296.042 233.37 319.958 254.63 341.329 230.588 365.37 251.958 386.63 228.042 362.588 206.671 383.958 182.63"
        className="ci-primary"
      />
    </svg>
  );
}
