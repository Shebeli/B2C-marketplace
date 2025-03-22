/**
 * Transform a camel string to snake case.
 */
function transformWordToSnakeCase(camelString: string) {
  const words = [];
  let j = 0;
  camelString.split("").map((letter, i) => {
    if (/^[A-Z]$/.test(letter)) {
      words.push(camelString.slice(j, i).toLowerCase());
      j = i;
    }
  });
  words.push(camelString.slice(j, camelString.length).toLowerCase());
  return words.join("_");
}

/**
 * Transform an object keys from camel case to snake case.
 * Used for mapping.
 */
export function transformKeysToSnakeCase(object: object) {
  return Object.fromEntries(
    Object.entries(object).map(([key, value]) => {
      return [transformWordToSnakeCase(key), value];
    })
  );
}
