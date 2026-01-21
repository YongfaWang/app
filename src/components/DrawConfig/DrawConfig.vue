<template>
  <div class="draw-config-container">
    <div class="config-panel">
      <t-form
        ref="form"
        :model="formData"
        :rules="formRules"
        layout="vertical"
        scroll-to-first-error="smooth"
        @submit="handleSubmit"
      >
        <t-form-item label="数据范围">
          <t-radio-group v-model="formData.rangeType" @change="handleRangeTypeChange">
            <t-radio value="all">全部数据</t-radio>
            <t-radio value="start-end">起始-结束位置</t-radio>
            <t-radio value="segments">分段选择</t-radio>
          </t-radio-group>
          
          <div v-if="formData.rangeType === 'start-end'" class="range-inputs">
            <t-input-number 
              v-model="formData.startIndex" 
              :min="0" 
              :max="dataLength - 1"
              placeholder="起始位置"
            />
            <span class="separator">至</span>
            <t-input-number 
              v-model="formData.endIndex" 
              :min="0" 
              :max="dataLength - 1"
              placeholder="结束位置"
            />
          </div>
          
          <div v-if="formData.rangeType === 'segments'" class="segments-container">
            <div v-for="(segment, index) in formData.segments" :key="index" class="segment-item">
              <t-input-number 
                v-model="segment.start" 
                :min="0" 
                :max="dataLength - 1"
                placeholder="起始"
              />
              <span class="separator">至</span>
              <t-input-number 
                v-model="segment.end" 
                :min="0" 
                :max="dataLength - 1"
                placeholder="结束"
              />
              <t-button variant="outline" @click="removeSegment(index)" v-if="formData.segments.length > 1">
                删除
              </t-button>
            </div>
            <t-button variant="outline" @click="addSegment">添加分段</t-button>
          </div>
        </t-form-item>
        
        <t-form-item v-if="lineCount > 1" label="显示线条" name="selectedLines">
          <t-checkbox-group v-model="formData.selectedLines" :options="lineOptions" />
        </t-form-item>
        
        <t-form-item>
          <t-button theme="primary" type="submit">确定</t-button>
          <t-button variant="outline" @click="resetForm">重置</t-button>
        </t-form-item>
      </t-form>
    </div>
    
    <div class="chart-container">
      <div ref="chartRef" style="width: 100%; height: 500px;"></div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';

export default {
  name: "DrawConfig",
  props: {
    content: {
      type: Object,
      default: () => ({})
    }
  },
  data() {
    return {
      formData: {
        rangeType: 'all',
        startIndex: 0,
        endIndex: 0,
        segments: [{ start: 0, end: 0 }],
        selectedLines: []
      },
      chartInstance: null,
      dataLength: 0,
      lineCount: 0,
      formRules: {
        dataRange: [
          { required: true, message: '请选择数据范围', trigger: 'blur' }
        ]
      }
    };
  },
  computed: {
    lineOptions() {
      return Array.from({ length: this.lineCount }, (_, i) => ({
        label: `线条 ${i + 1}`,
        value: i
      }));
    }
  },
  watch: {
    content: {
      handler(newVal) {
        if (newVal && newVal.shape) {
          this.initData();
        }
      },
      immediate: true,
      deep: true
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initChart();
    });
    window.addEventListener('resize', this.handleResize);
  },
  beforeDestroy() {
    if (this.chartInstance) {
      this.chartInstance.dispose();
    }
    window.removeEventListener('resize', this.handleResize);
  },
  methods: {
    initData() {
      if (!this.content.shape) return;
      
      // 处理shape数据，支持一维和二维数组
      const shape = this.content.shape;
      if (shape.length === 1) {
        // 一维数据，只有一根线条
        this.dataLength = shape[0];
        this.lineCount = 1;
      } else {
        // 二维数据，多根线条
        this.dataLength = shape[0];
        this.lineCount = shape[1];
      }
      
      // 设置默认值
      this.formData.endIndex = this.dataLength - 1;
      this.formData.segments[0].end = this.dataLength - 1;
      
      // 默认选中所有线条
      this.formData.selectedLines = Array.from({ length: this.lineCount }, (_, i) => i);
      
      // 初始化图表
      this.$nextTick(() => {
        this.updateChart();
      });
    },
    
    initChart() {
      if (!this.$refs.chartRef) {
        console.warn('Chart container not found');
        return;
      }
      
      try {
        this.chartInstance = echarts.init(this.$refs.chartRef);
        
        // 设置默认配置 - 优化小数值显示
        const option = {
          title: {
            text: '数据可视化图表',
            left: 'center'
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'cross'
            },
            // 自定义tooltip格式化，确保小数值正确显示
            formatter: (params) => {
              let result = `数据点: ${params[0].dataIndex}<br>`;
              params.forEach(param => {
                const value = param.value;
                let displayValue;
                
                // 处理小数值显示
                if (typeof value === 'number') {
                  if (Math.abs(value) < 1e-10) {
                    // 对于极小的值，使用科学计数法显示
                    displayValue = value.toExponential(4);
                  } else {
                    // 对于常规值，保留足够的小数位
                    displayValue = value.toFixed(12);
                  }
                } else {
                  displayValue = value;
                }
                
                result += `${param.seriesName}: ${displayValue}<br>`;
              });
              return result;
            }
          },
          legend: {
            data: [],
            bottom: 10
          },
          toolbox: {
            feature: {
              dataZoom: {
                yAxisIndex: false
              },
              restore: {},
              saveAsImage: {
                type: 'png',
                name: 'chart'
              }
            },
            right: 20
          },
          dataZoom: [
            {
              type: 'inside',
              start: 0,
              end: 100,
              xAxisIndex: [0]
            },
            {
              type: 'slider',
              start: 0,
              end: 100,
              xAxisIndex: [0]
            }
          ],
          grid: {
            left: '3%',
            right: '4%',
            bottom: '15%',
            containLabel: true
          },
          xAxis: {
            type: 'category',
            boundaryGap: false,
            name: '数据点',
            data: []
          },
          yAxis: {
            type: 'value',
            scale: true,
            name: '数值',
            // 优化小数值显示
            axisLabel: {
              formatter: (value) => {
                // 对于极小的值，使用科学计数法显示
                if (Math.abs(value) < 1e-10) {
                  return value.toExponential(2);
                }
                // 对于常规值，保留足够的小数位
                return value.toFixed(10);
              }
            }
          },
          series: []
        };
        
        this.chartInstance.setOption(option);
      } catch (error) {
        console.error('初始化图表失败:', error);
      }
    },
    
    updateChart() {
      if (!this.chartInstance || !this.content.data) {
        console.warn('图表实例或数据不存在');
        return;
      }
      
      try {
        const xAxisData = [];
        const seriesData = [];
        const legendData = [];
        
        // 生成X轴数据
        if (this.formData.rangeType === 'all') {
          for (let i = 0; i < this.dataLength; i++) {
            xAxisData.push(i);
          }
        } else if (this.formData.rangeType === 'start-end') {
          const start = this.formData.startIndex || 0;
          const end = this.formData.endIndex || this.dataLength - 1;
          for (let i = start; i <= end; i++) {
            xAxisData.push(i);
          }
        } else if (this.formData.rangeType === 'segments') {
          this.formData.segments.forEach(segment => {
            const start = segment.start || 0;
            const end = segment.end || this.dataLength - 1;
            for (let i = start; i <= end; i++) {
              if (!xAxisData.includes(i)) {
                xAxisData.push(i);
              }
            }
          });
          xAxisData.sort((a, b) => a - b);
        }
        
        // 如果没有选中任何线条，则默认选中所有
        const selectedLines = this.formData.selectedLines.length > 0 
          ? this.formData.selectedLines 
          : Array.from({ length: this.lineCount }, (_, i) => i);
        
        // 生成系列数据
        selectedLines.forEach(lineIndex => {
          const lineData = [];
          
          xAxisData.forEach(xIndex => {
            let value;
            
            // 根据数据结构获取数据
            if (this.content.shape.length === 1) {
              // 一维数据
              value = this.content.data[xIndex];
            } else {
              // 二维数据
              if (this.content.data[xIndex] && this.content.data[xIndex][lineIndex] !== undefined) {
                value = this.content.data[xIndex][lineIndex];
              } else {
                value = null;
              }
            }
            
            // 确保值为有效数字
            if (value !== null && value !== undefined && !isNaN(value)) {
              lineData.push(Number(value));
            } else {
              lineData.push('-');
            }
          });
          
          const seriesName = `线条 ${lineIndex + 1}`;
          seriesData.push({
            name: seriesName,
            type: 'line',
            data: lineData,
            smooth: true,
            symbol: 'none',
            connectNulls: false
          });
          
          legendData.push(seriesName);
        });
        
        // 更新图表
        const option = {
          legend: {
            data: legendData
          },
          xAxis: {
            data: xAxisData
          },
          yAxis: {
            // 动态调整Y轴范围以适应小数值
            min: () => {
              // 计算数据的最小值，稍微向下扩展一点范围
              const allData = seriesData.flatMap(series => series.data.filter(d => typeof d === 'number'));
              const minVal = allData.length > 0 ? Math.min(...allData) : 0;
              return minVal - Math.abs(minVal) * 0.1; // 向下扩展10%
            },
            max: () => {
              // 计算数据的最大值，稍微向上扩展一点范围
              const allData = seriesData.flatMap(series => series.data.filter(d => typeof d === 'number'));
              const maxVal = allData.length > 0 ? Math.max(...allData) : 0;
              return maxVal + Math.abs(maxVal) * 0.1; // 向上扩展10%
            }
          },
          series: seriesData
        };
        
        this.chartInstance.setOption(option, {
          notMerge: false
        });
        
      } catch (error) {
        console.error('更新图表失败:', error);
        this.$message.error('图表更新失败: ' + error.message);
      }
    },
    
    handleRangeTypeChange() {
      // 当范围类型改变时重置相关字段
      if (this.formData.rangeType === 'start-end') {
        this.formData.startIndex = 0;
        this.formData.endIndex = this.dataLength - 1;
      } else if (this.formData.rangeType === 'segments') {
        this.formData.segments = [{ start: 0, end: this.dataLength - 1 }];
      }
    },
    
    addSegment() {
      this.formData.segments.push({
        start: 0,
        end: this.dataLength - 1
      });
    },
    
    removeSegment(index) {
      this.formData.segments.splice(index, 1);
    },
    
    handleSubmit({ validateResult }) {
      if (validateResult === true) {
        this.updateChart();
        this.$message.success('配置已应用');
        
        // 输出表单数据用于调试
        console.log('表单数据:', JSON.parse(JSON.stringify(this.formData)));
      }
    },
    
    resetForm() {
      this.$refs.form.reset();
      this.initData();
    },
    
    handleResize() {
      if (this.chartInstance) {
        try {
          this.chartInstance.resize();
        } catch (error) {
          console.error('调整图表大小失败:', error);
        }
      }
    }
  }
};
</script>

<style scoped>
.draw-config-container {
  display: flex;
  height: 100%;
  gap: 20px;
}

.config-panel {
  width: 300px;
  flex-shrink: 0;
  padding: 16px;
  border-right: 1px solid #e7e7e7;
  overflow-y: auto;
}

.chart-container {
  flex: 1;
  padding: 16px;
  min-height: 0;
}

.range-inputs, .segment-item {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
}

.segment-item {
  margin-bottom: 8px;
}

.segments-container {
  margin-top: 8px;
}

.separator {
  margin: 0 4px;
  color: #999;
}
</style>