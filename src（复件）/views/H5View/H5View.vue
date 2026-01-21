<template>
  <t-layout>
    <t-header>
      <t-row>
        <t-col>
          <t-button @click="openFile" shape="rectangle" variant="outline">
            打开文件
          </t-button>
        </t-col>
        <t-col>
        </t-col>
      </t-row>
    </t-header>
    <t-list :split="true" style="max-height: 300px" stripe>
      <t-list-item>
        测试内容测试内容1
        <template #action>
          <span>
            <t-link theme="primary" hover="color" style="margin-left: 16px">绘图</t-link>
          </span>
        </template>
      </t-list-item>
      <t-list-item>
        测试内容测试内容2
        <template #action>
          <span>
            <t-link theme="primary" hover="color" style="margin-left: 16px">绘图</t-link>
          </span>
        </template>
      </t-list-item>
      <t-list-item>
        测试内容测试内容3
        <template #action>
          <span>
            <t-link theme="primary" hover="color" style="margin-left: 16px">绘图</t-link>
          </span>
        </template>
      </t-list-item>
      <t-list-item>
        测试内容测试内容4
        <template #action>
          <span>
            <t-link theme="primary" hover="color" style="margin-left: 16px">绘图</t-link>
          </span>
        </template>
      </t-list-item>
      <t-list-item>
        测试内容测试内容5
        <template #action>
          <span>
            <t-link theme="primary" hover="color" style="margin-left: 16px">绘图</t-link>
          </span>
        </template>
      </t-list-item>
      <t-list-item>
        测试内容测试内容5
        <template #action>
          <span>
            <t-link theme="primary" hover="color" style="margin-left: 16px">绘图</t-link>
          </span>
        </template>
      </t-list-item>
    </t-list>
    <t-footer v-if="isHiddenExecute" style="background-color: white; padding: 20px; display: flex; justify-content: end;">
      <t-button @click="handlerCancel" shape="rectangle" theme="defult" style="margin-right: 20px;">
        Cancel
      </t-button>
      <t-button @click="handlerSr" shape="rectangle" theme="primary">
        Save & Run
      </t-button>
    </t-footer>
  </t-layout>
</template>
<script>
const { ipcRenderer } = require('electron');
export default {
  name: 'H5View',
  components: {
  },
  created() {
    this.isHiddenExecute = !window.history.state.replaced;
  },
  data() {
    return {
      isHiddenExecute: true
    }
  },
  methods: {
    openFile() {
      ipcRenderer.on('openH5Complete', (event, files) => {
        console.log(files); // 输出选择的文件
      })
      // // 渲染进程
      // ipcRenderer.invoke('some-name', someArgument).then((result) => {
      //   // ...
      // })
      ipcRenderer.send('openH5');
    }
  }
}
</script>
<style></style>