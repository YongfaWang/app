<template>
  <div class="home-ex-container">
    <div class="content-wrapper">

      <div class="header-section">
        <h1 class="main-title">引力波卫星仿真与数据分析平台</h1>
        <p class="sub-title">轨道 · 信号 · 噪声 · 数据可视化的一体化仿真流程</p>
      </div>

      <div class="cards-section">
        <div class="cards-grid">
          <StepCard v-for="(card, index) in stepCards" :key="index" :stepText="card.stepText" :title="card.title"
            :description="card.description" :tags="card.tags" @onClick="pageRouter(card.router)" class="grid-item" />
        </div>
      </div>

      <div class="charts-section">
        <div class="chart-wrapper">
          <div class="chart-header">示例: 轨道距离变化</div>
          <div ref="chart1" class="echart-instance"></div>
        </div>

        <div class="chart-wrapper">
          <div class="chart-header">示例: 引力波信号 + 噪声</div>
          <div ref="chart2" class="echart-instance"></div>
        </div>
      </div>

      <div class="footer">
        © 2026 引力波卫星仿真平台 | 科研演示 / 教学 / 项目汇报
      </div>
    </div>
    <div>
      <t-dialog placement="center" v-model:visible="winconfig.workWeiget.isShow" :header="getCurrentWeightName"
        :confirmBtn="null" :cancelBtn="null" width="90vw" :onClose="closeDialog" height="80vh" :footer="null">
        <div style="height: 70vh; overflow: hidden;">
          <H5View @onCancel="closeDialog" v-if="this.winconfig.flag === 'h5view'" />
          <Glitchs @onCancel="closeDialog" v-else-if="this.winconfig.flag === 'glitchs'" />
          <GWResponse @onCancel="closeDialog" v-else-if="this.winconfig.flag === 'gwresponse'" />
          <Instrument @onCancel="closeDialog" v-else-if="this.winconfig.flag === 'instrument'" />
          <Orbits @onCancel="closeDialog" v-else-if="this.winconfig.flag === 'orbits'" />
        </div>
      </t-dialog>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import StepCard from '@/components/StepCard/StepCard';
import H5View from '@/views/H5View/H5View';
import Glitchs from '@/views/Glitchs/Glitchs';
import GWResponse from '@/views/GWResponse/GWResponse';
import Instrument from '@/views/Instrument/Instrument';
import Orbits from '@/views/Orbits/Orbits';
export default {
  name: 'HomeEx',
  components: {
    StepCard,
    H5View,
    Glitchs,
    GWResponse,
    Instrument,
    Orbits
  },
  data() {
    return {
      winconfig: {
        workWeiget: {
          isShow: false,
          flag: ""
        }
      },
      stepCards: [
        {
          stepText: 'STEP 01',
          title: 'Orbits',
          router: 'orbits',
          // description: '生成引力波卫星星座与航天器轨道，描述星间几何关系及其随时间演化。',
          description: 'Generate gravitational wave satellite constellations and spacecraft orbits, describe the geometric relationships between stars and their evolution over time.',
          tags: ['Orbit Dynamics', 'Constellation'],
        },
        {
          stepText: 'STEP 02',
          title: 'GW Response',
          router: 'gwresponse',
          // description: '构建不同类型引力波源模型，模拟星间测量链路对引力波的响应。',
          description: 'Construct different types of gravitational wave source models and simulate the response of inter-satellite measurement links to gravitational waves.',
          tags: ['GW Source', 'Response'],
        },
        {
          stepText: 'STEP 03',
          title: 'Glitches',
          router: 'glitchs',
          // description: '模拟激光系统中的瞬态异常信号，对数据质量与TDI性能进行评估。',
          description: 'Simulate transient anomalous signals in the laser system and evaluate data quality and TDI performance.',
          tags: ['Laser Glitch', 'Transient'],
        },
        {
          stepText: 'STEP 04',
          title: 'Instrument',
          router: 'instrument',
          // description: '构建加速度噪声、光学路径噪声与时钟噪声等关键误差源模型。',
          description: 'Construct key error source models such as acceleration noise, optical path noise, and clock noise.',
          tags: ['Instrument Noise', 'PSD'],
        },
        {
          stepText: 'STEP 05',
          title: 'H5View',
          router: 'h5view',
          // description: '对仿真生成的观测量进行可视化展示，支持时域与频域分析。',
          description: 'Visualize the simulated observation data and support time and frequency domain analysis.',
          tags: ['Visualization', 'Time & Frequency'],
        }
      ],
      chartInstance1: null,
      chartInstance2: null,
    };
  },
  mounted() {
    this.$nextTick(() => {
      this.initCharts();
      // window.addEventListener('resize', this.handleResize);
    });
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.handleResize);
    if (this.chartInstance1) this.chartInstance1.dispose();
    if (this.chartInstance2) this.chartInstance2.dispose();
  },
  methods: {
    pageRouter(flag) {
      this.winconfig.flag = flag
      this.winconfig.workWeiget.isShow = true
    },
    closeDialog() {
      console.log("关闭弹窗");

      this.winconfig.flag = ''
      this.winconfig.workWeiget.isShow = false
    },

    getCurrentWeightName() {
      switch (this.winconfig.flag) {
        case 'h5view':
          return "H5View"
        case 'glitchs':
          return "Glitchs Configure"
        case 'gwresponse':
          return "GW Response Configure"
        case 'instrument':
          return "Instrument Configure"
        case 'orbits':
          return "Orbits Configure"
      }
    },
    handleResize() {
      if (this.chartInstance1) this.chartInstance1.resize();
      if (this.chartInstance2) this.chartInstance2.resize();
    },
    initCharts() {
      this.initChart1();
      this.initChart2();
    },
    initChart1() {
      const chartDom = this.$refs.chart1;
      this.chartInstance1 = echarts.init(chartDom);

      // Generate some dummy sine wave data
      const data = [];
      for (let i = 0; i < 50; i++) {
        data.push([i, 2500000 + Math.sin(i / 2) * 20000 + Math.random() * 5000]);
      }

      const option = {
        backgroundColor: 'transparent',
        grid: { top: 40, right: 20, bottom: 20, left: 60, containLabel: true },
        tooltip: { trigger: 'axis' },
        legend: { data: ['Inter-satellite Distance (km)'], textStyle: { color: '#ccc' } },
        xAxis: {
          type: 'value',
          splitLine: { show: false },
          axisLabel: { color: '#888' }
        },
        yAxis: {
          type: 'value',
          min: 'dataMin',
          splitLine: { lineStyle: { color: '#333', type: 'dashed' } },
          axisLabel: { color: '#888' }
        },
        series: [
          {
            name: 'Inter-satellite Distance (km)',
            type: 'line',
            data: data,
            symbol: 'circle',
            symbolSize: 6,
            itemStyle: { color: '#4facfe' },
            lineStyle: { width: 2 }
          }
        ]
      };
      this.chartInstance1.setOption(option);
    },
    initChart2() {
      const chartDom = this.$refs.chart2;
      this.chartInstance2 = echarts.init(chartDom);

      // Generate noisy wave data
      const data = [];
      for (let i = 0; i < 200; i++) {
        data.push([i, Math.sin(i / 10) * 1e-21 + (Math.random() - 0.5) * 0.2e-21]);
      }

      const option = {
        backgroundColor: 'transparent',
        grid: { top: 40, right: 20, bottom: 20, left: 60, containLabel: true },
        tooltip: { trigger: 'axis' },
        legend: { data: ['GW + Noise'], textStyle: { color: '#ccc' } },
        xAxis: {
          type: 'value',
          splitLine: { show: false },
          axisLabel: { color: '#888' }
        },
        yAxis: {
          type: 'value',
          splitLine: { lineStyle: { color: '#333', type: 'dashed' } },
          axisLabel: { color: '#888' }
        },
        series: [
          {
            name: 'GW + Noise',
            type: 'line',
            data: data,
            symbol: 'circle',
            symbolSize: 4,
            showSymbol: false,
            itemStyle: { color: '#00f2fe' },
            lineStyle: { width: 1, color: '#00f2fe' }
          }
        ]
      };
      this.chartInstance2.setOption(option);
    }
  }
};
</script>

<style scoped lang="scss">
/* 1. Container Layout 
  Fixes the parent scroll issue by handling overflow internally
*/
.home-ex-container {
  width: 100%;
  height: 100%;
  /* Fills the parent height */
  background-color: var(--yf-color-1);
  /* Dark background from image */
  overflow-y: auto;
  /* Enable vertical scrolling */
  overflow-x: hidden;
  color: #ffffff;
  box-sizing: border-box;
}

.grid-item {
  box-shadow: 0 2px 8px var(--yf-shadow-color-1);
}

/* 2. Custom Scrollbar Styling 
  Rounded, no background track
*/
.home-ex-container::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.home-ex-container::-webkit-scrollbar-track {
  background: transparent;
  /* Remove background */
}

.home-ex-container::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  /* Rounded corners */
}

.home-ex-container::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* Content Wrapper to add padding */
.content-wrapper {
  padding: 40px;
  max-width: 1600px;
  /* Prevent it from getting too wide on huge screens */
  margin: 0 auto;
}

/* Header */
.header-section {
  text-align: center;
  margin-bottom: 50px;

  .main-title {
    color: var(--yf-color-2);
    font-size: 32px;
    font-weight: bold;
    margin-bottom: 12px;
    letter-spacing: 2px;
  }

  .sub-title {
    font-size: 16px;
    color: var(--td-text-color-secondary);
    letter-spacing: 1px;
  }
}

/* Cards Grid */
.cards-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  justify-content: center;
  margin-bottom: 40px;
}

/* Charts Section Layout */
.charts-section {
  display: flex;
  flex-wrap: wrap;
  /* Allows wrapping */
  gap: 24px;
  width: 100%;
}

.chart-wrapper {
  background: var(--yf-color-3);
  /* Slightly lighter card bg */
  border-radius: 12px;
  border: 1px solid #1f2738;
  padding: 20px;
  box-sizing: border-box;

  /* Flex magic for responsiveness */
  flex: 1;
  min-width: 500px;
  /* If space < 500px, it wraps to next line */
  height: 350px;
  display: flex;
  flex-direction: column;
}

/* Mobile adaptation for charts: 
  If screen is very small, allow chart to shrink below 500px 
*/
@media (max-width: 768px) {
  .chart-wrapper {
    min-width: 100%;
  }
}

.chart-header {
  font-size: 16px;
  color: #aeb9c4;
  margin-bottom: 10px;
  text-align: left;
}

.echart-instance {
  flex: 1;
  width: 100%;
  height: 100%;
}

/* Footer */
.footer {
  margin-top: 60px;
  text-align: center;
  color: var(--td-text-color-secondary);
  font-size: 12px;
}
</style>