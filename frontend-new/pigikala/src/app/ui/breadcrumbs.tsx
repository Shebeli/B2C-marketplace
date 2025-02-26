import Link from "next/link";

export interface breadcrumb {
  name: string;
  url: string;
}

export default function Breadcrumbs({
  breadcrumbs,
}: {
  breadcrumbs: breadcrumb[];
}) {
  return (
    <div className="breadcrumbs text-xs pt-2 pb-1">
      <ul>
        {breadcrumbs.map((bread) => (
          <li key={bread.name}>
            <Link href={bread.url}>{bread.name}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
