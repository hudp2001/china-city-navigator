// 用于加载和更新省市数据

// 检查是否为生产环境
const isProduction = import.meta.env.PROD

// 加载所有省份列表
export const loadAllProvinces = async () => {
  try {
    console.log('正在加载省份数据...')
    const response = await fetch('/assets/provinces.json')
    console.log('省份数据响应状态:', response.status)
    
    if (!response.ok) {
      throw new Error(`Network response was not ok. Status: ${response.status}`)
    }
    
    const data = await response.json()
    console.log('省份数据原始内容:', data)
    
    // 检查数据格式
    if (!data) {
      console.error('省份数据为空')
      return []
    }
    
    // 检查是否存在provinces字段
    if (data.provinces && Array.isArray(data.provinces)) {
      console.log(`成功加载 ${data.provinces.length} 个省份`)
      return data.provinces
    }
    
    // 如果没有provinces字段，但data本身是数组，则直接返回
    if (Array.isArray(data)) {
      console.log(`成功加载 ${data.length} 个省份`)
      return data
    }
    
    console.error('省份数据格式不正确:', data)
    return []
  } catch (error) {
    console.error('Error loading all provinces:', error)
    return []
  }
}

// 加载特定省份的详细数据
export const loadProvinceData = async (provinceId) => {
  try {
    const response = await fetch(`/assets/provinces/${provinceId}.json`)
    if (!response.ok) throw new Error('Network response was not ok')
    const data = await response.json()
    return data
  } catch (error) {
    console.error(`Error loading province data for ${provinceId}:`, error)
    return null
  }
}

// 加载所有省份的城市数据（用于热力图）
export const loadAllCities = async () => {
  try {
    const provinces = await loadAllProvinces()
    console.log('Provinces data:', provinces) // 调试信息
    
    // 检查provinces是否为数组
    if (!Array.isArray(provinces)) {
      console.error('Provinces is not an array:', provinces)
      return {}
    }
    
    const allCities = {}
    
    // 遍历所有省份
    for (const province of provinces) {
      // 检查province对象是否存在
      if (!province || !province.id) {
        console.warn('Invalid province data:', province)
        continue
      }
      
      try {
        const response = await fetch(`/assets/provinces/${province.id}.json`)
        if (response.ok) {
          const data = await response.json()
          
          // 处理每个城市数据，添加省份前缀以确保ID唯一性
          if (data.cities && Array.isArray(data.cities)) {
            data.cities.forEach(city => {
              // 检查城市数据是否有效
              if (!city || !city.id) {
                console.warn('Invalid city data:', city)
                return
              }
              
              // 为城市ID添加省份前缀以确保唯一性
              const uniqueId = `${province.id}_${city.id}`;
              
              allCities[uniqueId] = {
                ...city,
                id: uniqueId, // 使用唯一ID
                originalId: city.id, // 保存原始ID
                provinceId: province.id, // 添加省份ID
                name: city.name,
                location: city.location
              }
            })
          } else {
            console.warn(`No valid cities data for province ${province.name}`)
          }
        } else {
          console.warn(`Failed to load data for province ${province.name}:`, response.status)
        }
      } catch (error) {
        console.error(`加载${province.name}城市数据失败:`, error)
      }
    }
    
    console.log(`Successfully loaded ${Object.keys(allCities).length} cities`)
    return allCities
  } catch (error) {
    console.error('加载所有城市数据失败:', error)
    return {}
  }
}

// 加载特定省份的城市列表
export const loadCitiesByProvince = async (provinceId) => {
  try {
    const response = await fetch(`/assets/provinces/${provinceId}.json`)
    if (!response.ok) throw new Error('Network response was not ok')
    const data = await response.json()
    const cities = data.cities || []
    
    // 处理城市数据，添加标签信息，并确保城市ID唯一性（添加省份前缀）
    return cities.map(city => {
      // 为城市ID添加省份前缀以确保唯一性
      const uniqueId = `${provinceId}_${city.id}`;
      
      const tags = []
      
      // 添加景点标签
      if (city.attractions && city.attractions.length > 0) {
        tags.push({
          type: '景点',
          items: city.attractions
        })
      }
      
      // 添加美食标签（如果存在）
      if (city.cuisine && city.cuisine.length > 0) {
        tags.push({
          type: '美食',
          items: city.cuisine
        })
      }
      
      // 添加其他特征标签（如果存在）
      if (city.features && city.features.length > 0) {
        tags.push({
          type: '特色',
          items: city.features
        })
      }
      
      // 添加大学标签（如果存在）
      if (city.universities && city.universities.length > 0) {
        tags.push({
          type: '大学',
          items: city.universities
        })
      }
      
      // 添加商圈标签（如果存在）
      if (city.businessDistricts && city.businessDistricts.length > 0) {
        tags.push({
          type: '核心商圈',
          items: city.businessDistricts
        })
      }
      
      // 添加名人标签（如果存在）
      if (city.famousPeople && city.famousPeople.length > 0) {
        tags.push({
          type: '名人',
          items: city.famousPeople
        })
      }
      
      return {
        ...city,
        id: uniqueId, // 使用唯一ID
        originalId: city.id, // 保存原始ID
        provinceId, // 添加省份ID
        tags,
        // 如果城市数据中没有车牌号和身份证前缀，则使用默认值
        licensePlate: city.licensePlate ?? '未知',
        idPrefix: city.idPrefix ?? '未知',
        // 如果没有人均可支配收入和平均房价，则设置为null
        perCapitaDisposableIncome: city.perCapitaDisposableIncome ?? null,
        averageHousePrice: city.averageHousePrice ?? null,
        // 确保位置信息也被包含
        location: city.location ?? { lat: 0, lng: 0 }
      }
    })
  } catch (error) {
    console.error(`Error loading cities for province ${provinceId}:`, error)
    return []
  }
}

// 加载特定城市的详细数据
export const loadCityData = async (provinceId, cityId) => {
  try {
    const response = await fetch(`/assets/provinces/${provinceId}.json`)
    if (!response.ok) throw new Error('Network response was not ok')
    const data = await response.json()
    const cities = data.cities || []
    // 使用原始ID查找城市
    const city = cities.find(city => `${provinceId}_${city.id}` === cityId) || null
    
    if (!city) return null
    
    // 处理城市数据，添加标签信息
    const tags = []
    
    // 添加景点标签
    if (city.attractions && city.attractions.length > 0) {
      tags.push({
        type: '景点',
        items: city.attractions
      })
    }
    
    // 添加美食标签（如果存在）
    if (city.cuisine && city.cuisine.length > 0) {
      tags.push({
        type: '美食',
        items: city.cuisine
      })
    }
    
    // 添加大学标签（如果存在）
    if (city.universities && city.universities.length > 0) {
      tags.push({
        type: '大学',
        items: city.universities
      })
    }
    
    // 添加名人标签（如果存在）
    if (city.famousPeople && city.famousPeople.length > 0) {
      tags.push({
        type: '名人',
        items: city.famousPeople
      })
    }
    
    // 添加商圈标签（如果存在）- 放在最后
    if (city.businessDistricts && city.businessDistricts.length > 0) {
      tags.push({
        type: '核心商圈',
        items: city.businessDistricts
      })
    }
    
    // 为城市ID添加省份前缀以确保唯一性
    const uniqueId = `${provinceId}_${city.id}`;
    
    return {
      ...city,
      id: uniqueId, // 使用唯一ID
      originalId: city.id, // 保存原始ID
      provinceId, // 添加省份ID
      tags,
      // 如果城市数据中没有车牌号和身份证前缀，则使用默认值
      licensePlate: city.licensePlate || '未知',
      idPrefix: city.idPrefix || '未知',
      // 如果没有人均可支配收入和平均房价，则设置为null
      perCapitaDisposableIncome: city.perCapitaDisposableIncome || null,
      averageHousePrice: city.averageHousePrice || null,
      // 确保位置信息也被包含
      location: city.location
    }
  } catch (error) {
    console.error(`Error loading city data for ${cityId} in province ${provinceId}:`, error)
    return null
  }
}

export const updateAllProvinceData = async () => {
  // 实现一键更新所有省数据的逻辑
  console.log('Updating all province data...')
  // 这里可以添加实际的数据更新逻辑
}