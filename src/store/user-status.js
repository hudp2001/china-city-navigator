// 用于管理用户行为状态（收藏/去过/跑过）
export const getVisitedCities = () => {
  return JSON.parse(localStorage.getItem('visited') || '[]')
}

export const getCollectedCities = () => {
  return JSON.parse(localStorage.getItem('collected') || '[]')
}

export const getRanCities = () => {
  return JSON.parse(localStorage.getItem('ran') || '[]')
}

export const markVisited = (cityName) => {
  const visited = getVisitedCities()
  if (!visited.includes(cityName)) {
    visited.push(cityName)
    localStorage.setItem('visited', JSON.stringify(visited))
  }
}

export const markCollected = (cityName) => {
  const collected = getCollectedCities()
  if (!collected.includes(cityName)) {
    collected.push(cityName)
    localStorage.setItem('collected', JSON.stringify(collected))
  }
}

export const markRan = (cityName) => {
  const ran = getRanCities()
  if (!ran.includes(cityName)) {
    ran.push(cityName)
    localStorage.setItem('ran', JSON.stringify(ran))
  }
}