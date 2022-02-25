export default function circleMarker (feature, latlng) {
  return L.circleMarker(
    latlng,
    {
      radius: 7,
      fillColor: 'green',
      weight: 1,
      opacity: 1,
      fillOpacity: 1
    }
  )
}
