<template>
  <div style="height: 100%">
    <IniConfig
      v-show="showIniConfig"
      :content="xmlContent"
      title="GW Response Configure"
      @onSaveAndRun="onSaveAndRun"
      @onOnlySave="onOnlySave"
      @onCancel="onCancel"
      :isHiddenExecute="isHiddenExecute"
    ></IniConfig>
    <t-loading v-show="loading" />
    <div v-show="showLog" style="display: flex; flex-direction: column; height: 100%;">
      <div style="flex: 1; min-height: 0; overflow-y: auto;">
        <t-textarea v-model="logData" readonly :autosize="{ minRows: 10, maxRows: 50 }" style="height: 100%;"/>
      </div>
      <div
        style="
          background-color: white;
          padding: 20px;
          display: flex;
          justify-content: end;
          flex-shrink: 0;
        "
      >
        <t-button
          @click="
            showIniConfig = true;
            showLog = false;
          "
          shape="rectangle"
          theme="default"
          style="margin-right: 20px"
        >
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
    },
    // 保存并运行
    async onSaveAndRun({ localContent, pythonPath }) {
      this.saveXml(localContent)
      ipcRenderer.on("python-output", (_, data) => {
        this.logData += data;
      });
      ipcRenderer.on("python-end", () => {
        // this.runing = false;
      });
      this.logData = "";
      this.showIniConfig = false;
      this.loading = true;
      this.showLog = false;
      setTimeout(() => {
        console.log("asd");
        this.loading = false;
        this.running = true;
        this.showLog = true;
        MessagePlugin.success('Completed, need to check the output logs.')
      }, 1000);
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
        // this.runing = false;
      });
      this.logData = "";
      this.showIniConfig = false;
      this.loading = true;
      this.showLog = false;
      setTimeout(() => {
        console.log("asd");
        this.loading = false;
        this.running = true;
        this.showLog = true;
        MessagePlugin.success('Completed, need to check the output logs.')
      }, 1000);
      try {
        await ipcRenderer.invoke(
          "run-python",
          { pythonPath, scriptPath: (await ipcRenderer.invoke("getAppPath")) + this.pyPath }
        );
      } catch (error) {
        this.logData = `执行错误: ${error.message}`;
        // this.runing = false;
      }
    },
    onCancel() {
      this.$emit("onCancel");
    },
  },
};
</script>
<style></style>