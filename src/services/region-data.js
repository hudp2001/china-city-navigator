// 统一的省市数据结构，维护大区、省份和城市的正确关系
export const regionData = [
  {
    name: '华东地区',
    expanded: false, // 默认展开
    provinces: [
      {
        id: 'shanghai',
        name: '上海',
        center: [121.472644, 31.231706],
        zoom: 12,
        isMunicipality: true,
        cities: ['shanghai_city']
      },
      {
        id: 'jiangsu',
        name: '江苏',
        center: [118.767413, 32.041544],
        zoom: 8,
        cities: ['nanjing', 'suzhou', 'wuxi', 'xuzhou', 'changzhou', 'nantong', 'lianyungang', 'huaian', 'yancheng', 'yangzhou', 'zhenjiang', 'taizhou', 'suqian']
      },
      {
        id: 'zhejiang',
        name: '浙江',
        center: [120.153576, 30.287459],
        zoom: 8,
        cities: ['hangzhou', 'ningbo', 'wenzhou', 'jiaxing', 'huzhou', 'shaoxing', 'jinhua', 'quzhou', 'zhoushan', 'taizhou', 'lishui']
      },
      {
        id: 'anhui',
        name: '安徽',
        center: [117.283042, 31.86119],
        zoom: 8,
        cities: ['hefei', 'wuhu', 'bengbu', 'huainan', 'maanshan', 'huaibei', 'tongling', 'anqing', 'huangshan', 'chuzhou', 'fuyang', 'suzhou', 'luan', 'haozhou', 'chizhou', 'xuancheng']
      },
      {
        id: 'fujian',
        name: '福建',
        center: [119.296209, 26.076639],
        zoom: 8,
        cities: ['fuzhou', 'xiamen', 'putian', 'sanming', 'quanzhou', 'zhangzhou', 'nanping', 'longyan', 'ningde']
      },
      {
        id: 'jiangxi',
        name: '江西',
        center: [115.909228, 28.675697],
        zoom: 8,
        cities: ['nanchang', 'jingdezhen', 'pingxiang', 'jiujiang', 'xinyu', 'yingtan', 'ganzhou', 'jian', 'yiChun', 'fuZhou', 'shangRao']
      },
      {
        id: 'shandong',
        name: '山东',
        center: [117.000923, 36.675807],
        zoom: 8,
        cities: ['jinan', 'qingdao', 'zibo', 'zaozhuang', 'dongying', 'yantai', 'weifang', 'jining', 'taian', 'weihai', 'rizhao', 'laiwu', 'linyi', 'dezhou', 'liaocheng', 'binzhou', 'heze']
      }
    ]
  },
  {
    name: '华北地区',
    expanded: false, // 默认展开
    provinces: [
      {
        id: 'beijing',
        name: '北京',
        center: [116.405285, 39.904989],
        zoom: 12,
        isMunicipality: true,
        cities: ['beijing_city']
      },
      {
        id: 'tianjin',
        name: '天津',
        center: [117.190182, 39.125596],
        zoom: 12,
        isMunicipality: true,
        cities: ['tianjin_city']
      },
      {
        id: 'hebei',
        name: '河北',
        center: [114.502461, 38.045474],
        zoom: 8,
        cities: ['shijiazhuang', 'tangshan', 'qinhuangdao', 'handan', 'xingtai', 'baoding', 'zhangjiakou', 'chengde', 'cangzhou', 'langfang', 'hengshui']
      },
      {
        id: 'shanxi',
        name: '山西',
        center: [112.549248, 37.857014],
        zoom: 8,
        cities: ['taiyuan', 'datong', 'yangquan', 'changzhi', 'jincheng', 'shuozhou', 'jinzhong', 'yuncheng', 'xinzhou', 'linfen', 'lvliang']
      },
      {
        id: 'inner-mongolia',
        name: '内蒙古',
        center: [111.670801, 40.818311],
        zoom: 7,
        cities: ['hohhot', 'baotou', 'wuhai', 'chifeng', 'tongliao', 'ordos', 'hulunbuir', 'bayannaoer', 'ulanqab', 'xingan', 'xilingol', 'alxa']
      }
    ]
  },
  {
    name: '华南地区',
    expanded: false, // 默认折叠
    provinces: [
      {
        id: 'guangdong',
        name: '广东',
        center: [113.264385, 23.129112],
        zoom: 8,
        cities: ['guangzhou', 'shenzhen', 'zhuhai', 'shantou', 'foshan', 'jiangmen', 'zhanjiang', 'maoming', 'zhaoqing', 'huizhou', 'meizhou', 'shanwei', 'heyuan', 'yangjiang', 'qingyuan', 'dongguan', 'zhongshan', 'chaozhou', 'jieyang', 'yunfu']
      },
      {
        id: 'guangxi',
        name: '广西',
        center: [108.320004, 22.82402],
        zoom: 8,
        cities: ['nanning', 'liuzhou', 'guilin', 'wuzhou', 'beihai', 'fangchenggang', 'qinzhou', 'guigang', 'yulin', 'baise', 'hezhou', 'hechi', 'laibin', 'chongzuo']
      },
      {
        id: 'hainan',
        name: '海南',
        center: [110.33119, 20.031971],
        zoom: 8,
        cities: ['haikou', 'sanya', 'sanYa', 'wuzhishan', 'qionghai', 'danzhou', 'wenchang', 'wanning', 'dongfang', 'dingan', 'tunchang', 'cmal', 'lingao', 'baisha', 'changjiang', 'ledong', 'lingshui', 'baoting', 'qiongzhong']
      }
    ]
  },
  {
    name: '华中地区',
    expanded: false, // 默认折叠
    provinces: [
      {
        id: 'hubei',
        name: '湖北',
        center: [114.298572, 30.584355],
        zoom: 8,
        cities: ['wuhan', 'huangshi', 'shiyan', 'yichang', 'xiangyang', 'ezhou', 'jingmen', 'xiaogan', 'jingzhou', 'huanggang', 'xianning', 'suizhou', 'enshi', 'xiantao', 'qianjiang', 'tianmen', 'shennongjia']
      },
      {
        id: 'hunan',
        name: '湖南',
        center: [112.982279, 28.19409],
        zoom: 8,
        cities: ['changsha', 'zhuzhou', 'xiangtan', 'hengyang', 'shaoyang', 'yueyang', 'changde', 'zhangjiajie', 'yiyang', 'chenzhou', 'yongzhou', 'huaihua', 'loudi', 'xiangxi']
      },
      {
        id: 'henan',
        name: '河南',
        center: [113.665388, 34.757975],
        zoom: 8,
        cities: ['zhengzhou', 'kaifeng', 'luoyang', 'pingdingshan', 'anyang', 'hebi', 'xinxiang', 'jiaozuo', 'puyang', 'xuchang', 'luohe', 'sanmenxia', 'nanyang', 'shangqiu', 'xinyang', 'zhoukou', 'zhumadian', 'jiyuan']
      }
    ]
  },
  {
    name: '东北地区',
    expanded: false, // 默认折叠
    provinces: [
      {
        id: 'liaoning',
        name: '辽宁',
        center: [123.429096, 41.796948],
        zoom: 8,
        cities: ['shenyang', 'dalian', 'anshan', 'fushun', 'benxi', 'dandong', 'jinzhou', 'yingkou', 'fuxin', 'liaoyang', 'panjin', 'tieling', 'chaoyang', 'huludao']
      },
      {
        id: 'jilin',
        name: '吉林',
        center: [125.3245, 43.886841],
        zoom: 8,
        cities: ['changchun', 'jilin', 'siping', 'liaoyuan', 'tonghua', 'baishan', 'songyuan', 'baicheng', 'yanbian']
      },
      {
        id: 'heilongjiang',
        name: '黑龙江',
        center: [126.642464, 45.756967],
        zoom: 7,
        cities: ['haerbin', 'qiqihaer', 'jixi', 'hegang', 'shuangyashan', 'daqing', 'yichun', 'jiamusi', 'qitaihe', 'mudanjiang', 'heihe', 'suihua', 'daxinganling']
      }
    ]
  },
  {
    name: '西南地区',
    expanded: false, // 默认折叠
    provinces: [
      {
        id: 'chongqing',
        name: '重庆',
        center: [106.504962, 29.533155],
        zoom: 6,
        isMunicipality: true,
        cities: ['chongqing_city']
      },
      {
        id: 'sichuan',
        name: '四川',
        center: [104.065735, 30.659961],
        zoom: 7,
        cities: ['chengdu', 'zigong', 'panzhihua', 'luzhou', 'deyang', 'mianyang', 'guangyuan', 'suining', 'neijiang', 'leshan', 'nanchong', 'meishan', 'yibin', 'guangan', 'dazhou', 'yaan', 'bazhong', 'ziyang', 'aba', 'ganzi', 'liangshan']
      },
      {
        id: 'guizhou',
        name: '贵州',
        center: [106.713478, 26.578343],
        zoom: 8,
        cities: ['guiyang', 'liupanshui', 'zunyi', 'anshun', 'tongren', 'qianxinan', 'bijie', 'qiandongnan', 'qiannan']
      },
      {
        id: 'yunnan',
        name: '云南',
        center: [102.712251, 25.040609],
        zoom: 7,
        cities: ['kunming', 'qujing', 'yuxi', 'baoshan', 'zhaotong', 'lijiang', 'puer', 'lincang', 'chuxiong', 'honghe', 'wenshan', 'xishuangbanna', 'dadali', 'dehong', 'nujiang', 'diqing']
      },
      {
        id: 'tibet',
        name: '西藏',
        center: [91.132212, 29.660361],
        zoom: 7,
        cities: ['lasa', 'changdu', 'shannan', 'nyingchi', 'qamdo', 'ngari', 'nagqu']
      }
    ]
  },
  {
    name: '西北地区',
    expanded: false, // 默认折叠
    provinces: [
      {
        id: 'shanxi2', // 陕西
        name: '陕西',
        center: [108.948024, 34.263161],
        zoom: 7,
        cities: ['xian', 'tongchuan', 'baoji', 'xianyang', 'weinan', 'yanan', 'hanzhong', 'yulin', 'ankang', 'shangluo']
      },
      {
        id: 'gansu',
        name: '甘肃',
        center: [103.823557, 36.058039],
        zoom: 7,
        cities: ['lanzhou', 'jiayuguan', 'jinchang', 'baiyin', 'tianshui', 'wuwei', 'zhangye', 'pingliang', 'jiuquan', 'qingyang', 'dingxi', 'longnan', 'linxia', 'gannan']
      },
      {
        id: 'qinghai',
        name: '青海',
        center: [101.778916, 36.623177],
        zoom: 7,
        cities: ['xining', 'haidong', 'haibei', 'huangnan', 'hainan', 'guoluo', 'yushu', 'haixi']
      },
      {
        id: 'ningxia',
        name: '宁夏',
        center: [106.278179, 38.46637],
        zoom: 8,
        cities: ['yinchuan', 'shizuishan', 'wuzhong', 'guyuan', 'zhongwei']
      },
      {
        id: 'xinjiang',
        name: '新疆',
        center: [87.617733, 43.792818],
        zoom: 6,
        cities: ['wulumuqi', 'kelamayi', 'tulufan', 'hami', 'changji', 'boertala', 'bayinguoleng', 'akesu', 'kezilesu', 'kashen', 'hetian', 'yili', 'tacheng', 'aletai', 'shihezi', '阿拉尔', 'tumushuke', 'wujiaqu', 'beitun', 'tiemenguan', 'shuanghe', 'kokdala', 'kunyu', 'bishitun']
      }
    ]
  },
  {
    name: '港澳台地区',
    expanded: false, // 默认折叠
    provinces: [
      {
        id: 'hongkong',
        name: '香港',
        center: [114.173355, 22.320048],
        zoom: 11,
        isMunicipality: true,
        cities: ['hongkong_city']
      },
      {
        id: 'macau',
        name: '澳门',
        center: [113.54909, 22.198951],
        zoom: 12,
        isMunicipality: true,
        cities: ['macau_city']
      },
      {
        id: 'taiwan',
        name: '台湾',
        center: [121.509062, 25.044332],
        zoom: 8,
        cities: ['taipei', 'kaohsiung', 'tainan', 'taichung', 'nantou', 'hualien', 'ilan', 'miaoli', 'taoyuan', 'changhua', 'penghu', 'yunlin', 'keelung', 'hsinchu', 'chiayi']
      }
    ]
  }
]

// 根据省份ID获取省份信息
export const getProvinceById = (provinceId) => {
  for (const region of regionData) {
    const province = region.provinces.find(p => p.id === provinceId)
    if (province) {
      return {
        ...province,
        regionName: region.name
      }
    }
  }
  return null
}

// 获取所有省份列表
export const getAllProvinces = () => {
  const provinces = []
  regionData.forEach(region => {
    region.provinces.forEach(province => {
      provinces.push({
        ...province,
        regionName: region.name
      })
    })
  })
  return provinces
}