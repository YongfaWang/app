<template>
  <div style="height: 100%">
    <IniConfig
      v-show="showIniConfig"
      :content="iniContent"
      @onSaveAndRun="onSaveAndRun"
      @onOnlySave="onOnlySave"
      @onCancel="onCancel"
      :isHiddenExecute="isHiddenExecute"
    ></IniConfig>
    <t-loading v-show="loading" />
    <div v-show="showLog">
      <t-textarea v-model="logData" readonly autosize />
      <div
        style="
          background-color: white;
          padding: 20px;
          display: flex;
          justify-content: end;
        "
      >
        <t-button
          @click="
            showIniConfig = true;
            showLog = false;
          "
          shape="rectangle"
          theme="defult"
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
  name: "Orbits",
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
      iniContent: {},
      loading: false,
      runing: false,
      showIniConfig: true,
      logData: "",
      iniPath: "/lisa_sim/testorbits/orbits.ini",
      pyPath: "/lisa_sim/testorbits/main_orbits.py",
    };
  },
  methods: {
    async getData() {
      console.log(this.iniPath);
      this.iniContent = await ipcRenderer.invoke(
        "readIni",
        (await ipcRenderer.invoke("getAppPath")) + this.iniPath
      );
      this.iniContent = toRaw(this.iniContent);
      console.log(this.iniContent);
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
    async onSaveAndRun(localContent) {
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
          (await ipcRenderer.invoke("getAppPath")) + this.pyPath
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