// 城市状态管理服务

// 本地存储键名
const USER_STATUS_KEY = 'userCityStatus'

/**
 * 获取用户城市状态数据
 * @returns {Object} 用户城市状态对象
 */
export const getUserCityStatus = () => {
  try {
    const status = localStorage.getItem(USER_STATUS_KEY)
    return status ? JSON.parse(status) : {
      collected: [],  // 收藏的城市
      visited: [],    // 去过的城市
      ran: []         // 跑过的城市
    }
  } catch (error) {
    console.error('获取用户城市状态失败:', error)
    return {
      collected: [],
      visited: [],
      ran: []
    }
  }
}

/**
 * 保存用户城市状态数据
 * @param {Object} status 用户城市状态对象
 */
export const saveUserCityStatus = (status) => {
  try {
    localStorage.setItem(USER_STATUS_KEY, JSON.stringify(status))
  } catch (error) {
    console.error('保存用户城市状态失败:', error)
  }
}

/**
 * 检查城市是否具有某种状态
 * @param {string} cityId 城市ID（带省份前缀）
 * @param {string} type 状态类型 ('collected', 'visited', 'ran')
 * @returns {boolean} 是否具有该状态
 */
export const hasCityStatus = (cityId, type) => {
  const status = getUserCityStatus();
  // 精确匹配完整城市ID（含省份前缀）
  return status[type].some(id => id === cityId);
}

/**
 * 切换城市状态
 * @param {string} cityId 城市ID（带省份前缀）
 * @param {string} type 状态类型 ('collected', 'visited', 'ran')
 */
export const toggleCityStatus = (cityId, type) => {
  const status = getUserCityStatus();

  const index = status[type].findIndex(id => id === cityId);
  if (index > -1) {
    // 如果已存在，则移除
    status[type].splice(index, 1);
  } else {
    // 如果不存在，则添加
    status[type].push(cityId);
  }

  saveUserCityStatus(status);
}

/**
 * 获取所有标记为跑过的城市，用于热力图显示（含省份前缀）
 * @returns {Array} 城市ID数组
 */
export const getRanCities = () => {
  const status = getUserCityStatus();
  return [...status.ran];
}

/**
 * 获取所有标记为收藏的城市，用于热力图显示（含省份前缀）
 * @returns {Array} 城市ID数组
 */
export const getCollectedCities = () => {
  const status = getUserCityStatus();
  return [...status.collected];
}

/**
 * 获取所有标记为去过或跑过的城市，用于热力图显示（含省份前缀）
 * @returns {Array} 城市ID数组
 */
export const getVisitedAndRanCities = () => {
  const status = getUserCityStatus();
  const allCities = [...status.visited, ...status.ran];

  // 去重
  return [...new Set(allCities)];
}

/**
 * 获取所有标记为跑过的城市详情（含省份前缀）
 * @param {Object} allCitiesData 包含所有城市信息的对象，键为城市ID，值为城市对象
 * @returns {Array} 城市详情数组
 */
export const getRanCitiesDetails = (allCitiesData = {}) => {
  const ranCityIds = getRanCities();
  return ranCityIds.map(id => allCitiesData[id] || { id, name: id });
}

/**
 * 获取所有标记为收藏的城市详情（含省份前缀）
 * @param {Object} allCitiesData 包含所有城市信息的对象，键为城市ID，值为城市对象
 * @returns {Array} 城市详情数组
 */
export const getCollectedCitiesDetails = (allCitiesData = {}) => {
  const collectedCityIds = getCollectedCities();
  return collectedCityIds.map(id => allCitiesData[id] || { id, name: id });
}

/**
 * 获取所有标记为去过或跑过的城市详情（含省份前缀）
 * @param {Object} allCitiesData 包含所有城市信息的对象，键为城市ID，值为城市对象
 * @returns {Array} 城市详情数组
 */
export const getVisitedAndRanCitiesDetails = (allCitiesData = {}) => {
  const visitedCityIds = getVisitedAndRanCities();
  return visitedCityIds.map(id => allCitiesData[id] || { id, name: id });
}

/**
 * 清除所有用户城市状态
 */
export const clearAllCityStatus = () => {
  try {
    localStorage.removeItem(USER_STATUS_KEY)
  } catch (error) {
    console.error('清除用户城市状态失败:', error)
  }
}