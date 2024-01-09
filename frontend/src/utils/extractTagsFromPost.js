export default function extractTags(text) {
  const pattern = /(?<=[#])\w+/g
  return text.match(pattern)
}
