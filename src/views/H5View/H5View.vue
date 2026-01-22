<template>
  <t-layout style="height: 100%; display: flex; flex-direction: column;">
    <!-- 显示隐藏打开文件按钮 -->
    <t-header v-if="false" style="flex-shrink: 0;">
      <t-row>
        <t-col>
          <t-button @click="openFile" shape="rectangle" theme="primary" variant="outline">
            Open File
          </t-button>
        </t-col>
        <t-col>
        </t-col>
      </t-row>
    </t-header>

    <!-- 主要内容区域 -->
    <div v-if="currentDir.length != 0" style="flex: 1; display: flex; flex-direction: column; min-height: 0;">
      <!-- 面包屑导航区域 -->
      <div
        style="padding-left: 10px; padding-right: 10px; display: flex; flex-direction: row; justify-content: space-between; flex-shrink: 0;">
        <t-breadcrumb>
          <template v-slot:default>
            <t-breadcrumbItem v-for="(item, index) in currentPath" :key="index" @click="navTo(item)">{{ item
            }}</t-breadcrumbItem>
          </template>
          <template v-slot:separator> <chevron-right-icon name="chevron-right" />
          </template>
        </t-breadcrumb>
        <t-button :disabled="isRootDirectory" @click="goBack" shape="circle" variant="text">
          <rollback-icon :fill-color='"transparent"' :stroke-color='"currentColor"' :stroke-width="2" />
        </t-button>
      </div>
      <!-- 
      <t-list-item>
        <div style="width: 100%;">
          <span style="text-align: start; margin-left: calc(16px / 2); margin-right: calc(16px / 2);;">序号</span>
          <span style="text-align: center;">
            信息
          </span>
        </div>
        <template #action>
          <span>操作
          </span>
        </template>
      </t-list-item> -->
      <!-- 列表区域 -->
      <t-list :split="true" style="max-height: 100%; overflow-y: auto;" stripe>
        <t-list-item v-for="(item, index) in currentDir" :key="index">
          <div>
            <!-- <span style="margin-left: 16px; text-align: center;">{{ index }}</span> -->
            <span v-if="item.type === 'group'">
              <t-link @click="join(item)" hover="color"
                style="margin-left: 16px; font-weight: 400;font-family: 'SimHei', 'Heiti SC', sans-serif;">{{
                  item.name
                }}</t-link>
            </span>
            <span v-if="item.type === 'dataset'">
              <t-link @click="draw(item)" hover="color"
                style="margin-left: 16px; font-weight: 400;font-family: 'SimHei', 'Heiti SC', sans-serif;">{{
                  item.name
                }}</t-link>
            </span>
            <span>&nbsp;&nbsp;&nbsp;</span>
            <span v-if="item.type === 'dataset'" style="color: rgb(0 128 255);">{{ item.shape }}</span>
          </div>
          <template #action>
            <span>
              <t-link @click="join(item)" v-if="item.type === 'group'" theme="primary" hover="color"
                style="margin-left: 16px">Enter</t-link>
              <t-link @click="draw(item)" v-else-if="item.type === 'dataset'" theme="primary" hover="color"
                style="margin-left: 16px">Draw</t-link>
            </span>
          </template>
        </t-list-item>
      </t-list>
    </div>

    <!-- 空状态区域 -->
    <div v-else class="openfile" @click="openFile"
      style="flex: 1; display: flex; flex-direction: column; justify-content: center; align-items: center;">
      <div class="openfile-content">
        <FileAttachmentIcon style="margin-right: 5px;" size="20px" :fill-color='"transparent"'
          :stroke-color='"currentColor"' :stroke-width="2.5" />
        <span>Please open an HDF5 (*. h5) file</span>
      </div>
    </div>
    <t-dialog placement="center" v-model:visible="isVisibleDrawConfig" header="画图配置" :confirmBtn="null"
      :cancelBtn="null" width="60vw" height="50vh" :footer="null">
      <div style="height: 50vh; overflow: hidden;">
        <DrawConfig :content="drawContent" />
      </div>
    </t-dialog>
  </t-layout>
</template>
<script>
const { ipcRenderer } = require('electron');
import DrawConfig from '@/components/DrawConfig/DrawConfig';
// const H5 = require("node_modules/h5wasm/dist/esm/hdf5_hl.js")
// import * as hdf5 from "https://cdn.jsdelivr.net/gh/bmaranville/h5wasm@publish/dist/hdf5_hl.js";
import { ChevronRightIcon, RollbackIcon, FileAttachmentIcon } from 'tdesign-icons-vue-next';

export default {
  name: 'H5View',
  components: {
    ChevronRightIcon,
    RollbackIcon,
    FileAttachmentIcon,
    DrawConfig
  },
  created() {
  },
  data() {
    return {
      isVisibleDrawConfig: false,
      rawH5Tree: {},
      currentDir: [],
      currentPath: ["/"], // 改为数组形式，便于操作
      currentFullPath: "/" // 添加完整路径记录
    }
  },
  computed: {
    // 计算属性判断是否是根目录
    isRootDirectory() {
      return this.currentPath.length <= 1 ||
        (this.currentPath.length === 1 && this.currentPath[0] === '/');
    }
  },
  methods: {
    openFile() {
      ipcRenderer.on('openH5Complete', (event, files) => {
        console.log(files); // 输出选择的文件
        // this.filePath = "/home/wang/Downloads/RectangleGlitch.h5" // test file
        this.filePath = files
        this.readH5()
      })
      ipcRenderer.send('openH5');
    },
    async readH5() {
      this.currentDir = []
      var pythonPath = JSON.parse(localStorage.getItem("appSettings")).pythonPath
      this.rawH5Tree = await ipcRenderer.invoke(
        "readH5",
        { pythonPath, filePath: this.filePath }
      )
      console.log(this.rawH5Tree);
      if (this.rawH5Tree.type === "group") {

        this.currentPath = this.rawH5Tree.path === '/' ? '/' : this.rawH5Tree.path.split('/')
        this.rawH5Tree.children.forEach(item => {
          if (item.type === "group") {
            this.currentDir.push({
              name: item.name,
              type: "group",
              path: item.path
            })
          } else if (item.type === "dataset") {
            this.currentDir.push({
              name: item.name,
              type: "dataset",
              shape: item.shape,
              path: item.path
            })
          }
        });
      }
    },
    // 更新当前目录显示
    updateCurrentDir(node) {
      if (node?.type === "group" && node.children) {
        this.currentDir = node.children.map(child => ({
          name: child.name,
          type: child.type,
          shape: child.shape,
          path: child.path
        }));
      }
    },
    async draw(item) {
      var pythonPath = JSON.parse(localStorage.getItem("appSettings")).pythonPath
      this.drawContent = await ipcRenderer.invoke("readH5Dataset", { pythonPath, filePath: this.filePath, datasetPath: item.path })
      this.isVisibleDrawConfig = true
    },
    join(item) {
      console.log("切换前路径: ", item.path);

      const findNode = (node, path) => {
        if (node.path === path) return node;
        if (!node.children) return null;

        for (let child of node.children) {
          const result = findNode(child, path);
          if (result) return result;
        }
        return null;
      };

      const targetNode = findNode(this.rawH5Tree, item.path);

      if (targetNode?.type === "group" && targetNode.children) {
        // 更新当前目录
        this.updateCurrentDir(targetNode);

        // 更新面包屑路径
        this.currentPath = targetNode.path === '/'
          ? ['/']
          : ['/', ...targetNode.path.split('/').filter(Boolean)];
        this.currentFullPath = targetNode.path;
      }

      console.log("切换后路径: ", this.currentPath);
    },
    // 返回上一级
    goBack() {
      if (this.isRootDirectory) return;

      // 构建上一级路径
      const parentPath = this.currentPath.slice(0, -1);
      if (parentPath.length === 0) return;

      const parentFullPath = parentPath.length === 1 ? '/' : parentPath.slice(1).join('/');

      const findNode = (node, path) => {
        if (node.path === path) return node;
        if (!node.children) return null;

        for (let child of node.children) {
          const result = findNode(child, path);
          if (result) return result;
        }
        return null;
      };

      const parentNode = findNode(this.rawH5Tree, parentFullPath);

      if (parentNode) {
        this.currentPath = parentPath;
        this.currentFullPath = parentFullPath;
        this.updateCurrentDir(parentNode);
      }
    },
    navTo(item) {
      // 如果点击的是根目录
      if (item === '/') {
        this.currentPath = ['/'];
        this.currentFullPath = '/';
        this.updateCurrentDir(this.rawH5Tree);
        return;
      }

      // 查找点击的面包屑项在路径中的索引
      const targetIndex = this.currentPath.indexOf(item);

      // 如果点击的是当前路径中的某一级（非最后一级）
      if (targetIndex !== -1 && targetIndex < this.currentPath.length - 1) {
        // 构建目标路径（截取到点击的那一级）
        const targetPath = this.currentPath.slice(0, targetIndex + 1);
        const targetFullPath = targetPath.length === 1 ? '/' : targetPath.slice(1).join('/');

        this.currentPath = targetPath;
        this.currentFullPath = targetFullPath;

        const findNode = (node, path) => {
          if (node.path === path) return node;
          if (!node.children) return null;

          for (let child of node.children) {
            const result = findNode(child, path);
            if (result) return result;
          }
          return null;
        };

        const targetNode = findNode(this.rawH5Tree, targetFullPath);
        this.updateCurrentDir(targetNode);
      }
    },
  }
}
</script>
<style>
.openfile {
  height: 100%;
  cursor: pointer;
  transition: background-color .3s;
  display: flex;
  justify-content: center;
  align-items: center;
}

.openfile-content {
  display: flex;
  align-items: center;
  justify-content: center;
}

.openfile:hover {
  background-color: rgb(189, 189, 189);
  transition: background-color .3s;
}

.openfile:active {
  background-color: rgb(126, 126, 126);
  transition: background-color .3s;
}
</style>