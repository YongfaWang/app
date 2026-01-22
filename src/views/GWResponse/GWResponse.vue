<template>
  <div style="height: 100%">
    <IniConfig v-show="showIniConfig" :content="xmlContent" title="GW Response Configure" @onSaveAndRun="onSaveAndRun"
      @onOnlySave="onOnlySave" @onCancel="onCancel" :isHiddenExecute="isHiddenExecute"></IniConfig>
    <t-loading v-if="loading" class="loading-fixed" />
    <div v-show="showLog" class="log-wrapper">
      <t-textarea v-model="logData" readonly class="log-textarea" />

      <div class="log-actions">
        <t-button @click="copyLog" shape="rectangle" theme="default" style="margin-right: 20px">
          Copy Log
        </t-button>
        <t-button @click="showIniConfig = true; showLog = false;" shape="rectangle" theme="default"
          style="margin-right: 20px">
          Return
        </t-button>
      </div>
    </div>
  </div>
</template>
<script>
import { ipcRenderer } from "electron";
import { toRaw } from "vue";
import IniConfig from "@/components/IniConfig/IniConfig";
import { MessagePlugin } from 'tdesign-vue-next';
export default {
  name: "GWResponse",
  components: {
    IniConfig,
  },
  created() {
    this.isHiddenExecute = !window.history.state.replaced;
    this.getData();
  },
  data() {
    return {
      isHiddenExecute: true,
      xmlContent: {},
      loading: false,
      runing: false,
      showIniConfig: true,
      logData: "",
      xmlPath: "/lisa_sim/tests-gw-response/gw_response.xml",
      pyPath: "/lisa_sim/tests-gw-response/main_response.py",
    };
  },
  methods: {
    async copyLog() {
      try {
        await navigator.clipboard.writeText(this.logData);
        MessagePlugin.success('Log copied to clipboard!');
      } catch (err) {
        MessagePlugin.error('Failed to copy log: ' + err);
      }
    },
    async getData() {
      console.log(this.xmlPath);
      this.xmlContent = await ipcRenderer.invoke(
        "readXml",
        (await ipcRenderer.invoke("getAppPath")) + this.xmlPath
      );
      this.xmlContent = toRaw(this.xmlContent);
      console.log(this.xmlContent);
    },

    async saveXml(localContent) {
      // 保存后出现错误
      if (
        !(await ipcRenderer.invoke("saveXml", {
          filePath: (await ipcRenderer.invoke("getAppPath")) + this.xmlPath,
          content: toRaw(localContent),
        }))
      ) {
        console.err("Save Error.");
      }
    },
    onOnlySave(localContent) {
      this.saveXml(localContent);
      MessagePlugin.success('Completed!')
      this.$emit("onCancel");
    },
    // 保存并运行
    async onSaveAndRun({ localContent, pythonPath }) {
      this.saveXml(localContent)
      // 先移除之前的监听，避免重复添加监听器，导致多次响应，否则日志会重复出现多次
      ipcRenderer.removeAllListeners("python-output");
      ipcRenderer.removeAllListeners("python-end");
      /**
       * logData: 日志内容
       * showIniConfig: 是否显示配置界面
       * loading: 是否显示加载中
       * showLog: 是否显示日志界面
       * 
       * 执行前显示配置界面
       * 模拟加载, loading = true, 模拟1000ms后停止加载
       * loading结束后显示日志界面
       */
      this.logData = "";  // 日志内容
      this.showIniConfig = false; // 隐藏配置界面
      this.loading = true;
      this.showLog = false;     // 隐藏日志界面
      // 保存后出现错误
      if (
        !(await ipcRenderer.invoke("saveXml", {
          filePath: (await ipcRenderer.invoke("getAppPath")) + this.xmlPath,
          content: toRaw(localContent),
        }))
      ) {
        console.err("Save Error.");
      }
      ipcRenderer.on("python-output", (_, data) => {
        this.logData += data;
      });
      ipcRenderer.on("python-end", () => {
        this.runing = false;
      });
      setTimeout(() => {
        this.loading = false;
        this.showLog = true;
        MessagePlugin.success('Start running...')
      }, 1000);
      try {
        await ipcRenderer.invoke(
          "run-python",
          { pythonPath, scriptPath: (await ipcRenderer.invoke("getAppPath")) + this.pyPath }
        );
      } catch (error) {
        this.logData = `执行错误: ${error.message}`;
        this.runing = false;
      }
    },
    onCancel() {
      this.$emit("onCancel");
    },
  },
};
</script>
<style>
.loading-fixed {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 9999;
}

.log-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
  /* 🚫 外层永远不允许滚动 */
}

.log-textarea {
  flex: 1;
  /* ✅ 占满剩余高度 */
  height: 100%;
}

/* 强制内部 textarea 填满并滚动 */
.log-textarea textarea {
  height: 100% !important;
  resize: none;
  overflow-y: auto;
}

.log-actions {
  flex-shrink: 0;
  background: white;
  padding: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>