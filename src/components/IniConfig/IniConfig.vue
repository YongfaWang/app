<template>
  <t-layout style="height: 100%; display: flex; flex-direction: column;">
    <t-header v-if="isHiddenExecute" style="flex-shrink: 0;">
      <span style="font-size: 13pt; font-weight: bold">{{ title }}</span>
    </t-header>
    <t-content style="flex: 1; min-height: 0; background: var(--td-bg-color-container);">
      <div style="padding: 15px; height: calc(100% - 30px); display: flex; flex-direction: column;">
        <!-- 表单区域，设置可滚动 -->
        <div style="flex: 1; min-height: 0; overflow-y: auto; margin-bottom: 20px;">
          <t-form :data="localContent" label-width="120px" style="width: 100%; min-width: 800px;">
            <t-card v-for="(node, index) in localContent.node" :key="index" :title="node.name || node.comment"
              hover-shadow :style="{
                'margin-bottom': '20px',
                'background-color': index % 2 === 1 ? '#DDF4D9' : '#DBDBFF'
              }">
              <!-- 处理第一层节点（如 comments, glitches_types, glitches_parameters） -->
              <template #actions>
                <t-tooltip v-if="node.comment" :content="node.comment">
                  <HelpCircleIcon style="margin-left: 10px;" :fill-color='"transparent"' :stroke-width="2.5" />
                </t-tooltip>
              </template>
              <template v-if="node.node && Array.isArray(node.node)">
                <t-form-item v-for="(childNode, childIndex) in node.node" :key="childIndex"
                  :label="childNode.name || childNode.comment || formatName(childNode.name)">
                  <!-- 处理多选框类型 -->
                  <template v-if="childNode.type === 'check' && childNode.options">
                    <div class="checkbox-group">
                      <t-checkbox v-for="option in childNode.options.split(',')" :key="option" :value="option"
                        :checked="isOptionSelected(childNode.value, option)"
                        @change="handleCheckboxChange(childNode, option, $event)">
                        {{ option }}
                      </t-checkbox>
                      <t-tooltip v-if="childNode.comment" :content="childNode.comment">
                        <HelpCircleIcon style="margin-left: 10px;" :fill-color='"transparent"' :stroke-color='"#0006"'
                          :stroke-width="2.5" />
                      </t-tooltip>
                    </div>
                  </template>
                  <template v-else-if="childNode.type === 'select' && childNode.options">
                    <t-select :value="childNode.value" @change="handleSelectChange(childNode, $event)" placeholder="">
                      <t-option v-for="option in childNode.options.split(',')" :key="option" :value="option"
                        :label="option" />
                    </t-select>
                    <t-tooltip v-if="childNode.comment" :content="childNode.comment">
                      <HelpCircleIcon style="margin-left: 10px;" :fill-color='"transparent"' :stroke-color='"#0006"'
                        :stroke-width="2.5" />
                    </t-tooltip>
                  </template>
                  <template v-else-if="childNode.type === 'group' && childNode.group">
                    <div class="checkbox-group" v-for="(groupItem, groupIndex) in childNode.group" :key="groupIndex">
                      <t-checkbox v-for="option in groupItem.options.split(',')" :key="option" :value="option"
                        :checked="isOptionSelected(groupItem.value, option)"
                        @change="handleCheckboxChange(groupItem, option, $event)">
                        {{ option }}
                      </t-checkbox>
                      <t-tooltip v-if="groupItem.comment" :content="groupItem.comment">
                        <HelpCircleIcon style="margin-left: 10px;" :fill-color='"transparent"' :stroke-color='"#0006"'
                          :stroke-width="2.5" />
                      </t-tooltip>
                    </div>
                  </template>
                  <template v-else>
                    <t-input v-model="childNode.value" :type="getInputType(childNode.type)" />
                    <t-tooltip v-if="childNode.comment" :content="childNode.comment">
                      <HelpCircleIcon style="margin-left: 10px;" :fill-color='"transparent"' :stroke-color='"#0006"'
                        :stroke-width="2.5" />
                    </t-tooltip>
                  </template>
                </t-form-item>
              </template>
              <template v-else-if="node.node.type === 'check' && node.node.options">
                <div class="checkbox-group">
                  <t-checkbox v-for="option in node.node.options.split(',')" :key="option" :value="option"
                    :checked="isOptionSelected(node.node.value, option)"
                    @change="handleCheckboxChange(node.node, option, $event)">
                    {{ option }}
                  </t-checkbox>
                  <t-tooltip v-if="node.node.comment" :content="node.node.comment">
                    <HelpCircleIcon style="margin-left: 10px;" :fill-color='"transparent"' :stroke-color='"#0006"'
                      :stroke-width="2.5" />
                  </t-tooltip>
                </div>
              </template>
              <template v-else-if="node.node.type === 'select' && node.node.options">
                <t-select :value="node.node.value" @change="handleSelectChange(node.node, $event)" placeholder="">
                  <t-option v-for="option in node.node.options.split(',')" :key="option" :value="option"
                    :label="option" />
                </t-select>
              </template>
              <!-- 处理简单值的情况 -->
              <template v-else>
                <!-- 一层 -->
                <t-form-item :label="node.name" v-if="node.type != 'node'">
                  <t-input v-model="node.value" :type="getInputType(node.type)" />
                  <t-tooltip v-if="node.comment" :content="node.comment">
                    <HelpCircleIcon style="margin-left: 10px;" :fill-color='"transparent"' :stroke-color='"#0006"'
                      :stroke-width="2.5" />
                  </t-tooltip>
                </t-form-item>
                <!-- 二层 -->
                <t-form-item :label="node.node.name" v-else>
                  <t-input v-model="node.node.value" :type="getInputType(node.node.type)" />
                  <t-tooltip v-if="node.node.comment" :content="node.node.comment">
                    <HelpCircleIcon style="margin-left: 10px;" :fill-color='"transparent"' :stroke-color='"#0006"'
                      :stroke-width="2.5" />
                  </t-tooltip>
                </t-form-item>
              </template>
            </t-card>
          </t-form>
        </div>
        <div style="
            background-color: var(--td-bg-color-container);
            padding: 20px;
            display: flex;
            justify-content: end;
          ">
          <t-button v-if="!isHiddenExecute" @click="handlerCancel" shape="rectangle" theme="defult">
            Cancel
          </t-button>
          <t-button style="margin: 0 20px 0 20px" @click="handlerSave" shape="rectangle" variant="outline">
            <template #icon>
              <save-icon :fill-color='"transparent"' :stroke-color='"currentColor"'
                :stroke-width="2.5" /></template>Only
            Save
          </t-button>
          <t-button @click="handlerSr" shape="rectangle" theme="primary">
            <template #icon>
              <play-circle-stroke-icon :fill-color='"transparent"' :stroke-color='"currentColor"'
                :stroke-width="2.5" /></template>
            Save & Run
          </t-button>
        </div>
      </div>
    </t-content>
  </t-layout>
</template>

<script>
import { HelpCircleIcon, SaveIcon, PlayCircleStrokeIcon } from "tdesign-icons-vue-next"
export default {
  name: "IniConfig",
  props: {
    title: {
      type: String,
      required: false,
      default: ''
    },
    content: Object,
    isHiddenExecute: {
      type: Boolean,
      default: false,
    },
  },
  components: {
    HelpCircleIcon,
    SaveIcon,
    PlayCircleStrokeIcon
  },
  created() { },
  data() {
    return {
      localContent: {},
    };
  },
  watch: {
    content: {
      handler(newVal) {
        this.localContent = JSON.parse(JSON.stringify(newVal));
        console.log(this.localContent);
      },
      deep: true,
    },
  },
  methods: {
    getInputType(nodeType) {
      const typeMap = {
        'number': 'number',
        'float': 'number',
        'text': 'text'
      };
      return typeMap[nodeType] || 'text';
    },
    isOptionSelected(currentValue, option) {
      if (!currentValue) return false;
      // 假设currentValue是逗号分隔的字符串
      return currentValue.split(',').includes(option);
    },
    handleSelectChange(node, value) {
      node.value = value;
    },
    handleCheckboxChange(childNode, option, checked) {
      console.log(childNode);
      let currentValues = childNode.value ? childNode.value.split(',') : [];

      if (checked) {
        // 添加选项
        if (!currentValues.includes(option)) {
          currentValues.push(option);
        }
      } else {
        // 移除选项
        currentValues = currentValues.filter(val => val !== option);
      }

      // 更新值
      childNode.value = currentValues.join(',');

    },
    formatName(name) {
      // 你的格式化名称逻辑
      return name ? name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()) : '';
    },
    handlerCancel() {
      this.$emit("onCancel");
    },
    handlerSr() {
    var appSettings = JSON.parse(localStorage.getItem("appSettings"));
      this.$emit("onSaveAndRun", { localContent: this.localContent, pythonPath: appSettings.pythonPath });
    },
    handlerSave() {
      this.$emit("onOnlySave", this.localContent);
    },
  },
};
</script>

<style>

</style>
