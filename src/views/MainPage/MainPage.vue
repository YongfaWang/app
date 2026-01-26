<template>
  <t-layout style="height: 100%;">
    <t-header>
      <t-head-menu value="item1" height="120px">
        <template #logo>
          <img width="136" class="logo" src="/logo.jpg" alt="logo" />
        </template>
        <t-menu-item value="item1">
          <template #icon>
            <t-icon name="window" />
          </template>Window Mode</t-menu-item>
        <!-- <t-menu-item value="item2">大屏模式</t-menu-item> -->
        <template #operations>
          <t-tooltip content="Home">
            <t-button class="t-demo-collapse-btn" variant="text" shape="square" @click="routerHome">
              <template #icon><t-icon name="home" /></template>
            </t-button>
          </t-tooltip>
          <t-tooltip v-if="isFullScreen" content="Exit FullScreen">
            <t-button class="t-demo-collapse-btn" variant="text" shape="square" @click="fullscreen">
              <template #icon><t-icon name="fullscreen-exit" /></template>
            </t-button>
          </t-tooltip>
          <t-tooltip v-if="!isFullScreen" content="FullScreen">
            <t-button class="t-demo-collapse-btn" variant="text" shape="square" @click="fullscreen">
              <template #icon><t-icon name="fullscreen-2" /></template>
            </t-button>
          </t-tooltip>
          <t-tooltip content="Settings">
            <t-button class="t-demo-collapse-btn" variant="text" shape="square" @click="settingDialogVisible = true">
              <template #icon><t-icon name="setting" /></template>
            </t-button>
          </t-tooltip>
        </template>
      </t-head-menu>
    </t-header>
    <t-layout style="height: calc(100% - 64px)">
      <t-aside style="border-top: 1px solid var(--component-border);">
        <!-- default-expanded="['2-1']" 默认展开Tools -->
        <t-menu default-expanded="['2-1']" theme="light" v-model="currentMenu" :collapsed="collapsed"
          @change="changeHandler">
          <!-- <template #logo>
          <img :width="collapsed ? 35 : 136" :src="iconUrl" alt="logo" />
        </template> -->
          <t-menu-group title="Main">
            <t-menu-item value="home">
              <template #icon>
                <t-icon name="home" />
              </template>
              Home
            </t-menu-item>
          </t-menu-group>
          <t-menu-group title="Operation">
            <t-submenu title="Tools" value="2-1">
              <template #icon>
                <!-- <t-icon name="tools" /> -->
                <t-icon name="app" />
              </template>
              <t-menu-item value="orbits">Orbits</t-menu-item>
              <t-menu-item value="gwresponse">GW Response</t-menu-item>
              <t-menu-item value="instrument">Instrument</t-menu-item>
              <t-menu-item value="h5view">H5 View</t-menu-item>
              <t-menu-item value="glitchs">Glitchs</t-menu-item>
            </t-submenu>
            <t-menu-item value="2-2">
              <template #icon>
                <t-icon name="edit-1" />
              </template>
              Test1_placeholder
            </t-menu-item>
            <t-menu-item value="2-3">
              <template #icon>
                <t-icon name="root-list" />
              </template>
              Test2_placeholder
            </t-menu-item>
            <t-menu-item value="2-4">
              <template #icon>
                <t-icon name="check" />
              </template>
              Test3_placeholder
            </t-menu-item>
          </t-menu-group>
          <t-menu-group title="More">
            <t-menu-item value="item4">
              <template #icon>
                <t-icon name="help" />
              </template>
              Guide_placeholder
            </t-menu-item>
          </t-menu-group>
          <template #operations>
            <t-button class="t-demo-collapse-btn" variant="text" shape="square" @click="quitDialogVisible = true">
              <template #icon><t-icon name="login" /></template>
            </t-button>
          </template>
        </t-menu>
      </t-aside>
      <t-layout>
        <t-content style="height: calc(100% - 64px)">
          <RouterView v-slot="{ Component }" @itemClicked="handleItemClicked" @returnClicked="routerHome">
            <transition name="fade">
              <component :is="Component" />
            </transition>
          </RouterView>
        </t-content>
        <!-- <t-footer>Copyright @ 2019-{{ new Date().getFullYear() }} [---------------]. All Rights Reserved</t-footer> -->
      </t-layout>
    </t-layout>
    <t-dialog placement="center" v-model:visible="settingDialogVisible" header="Settings" @confirm="saveSettings" cancel-btn="Cancel" confirm-btn="OK">
      <template #default>
        <div class="settings-grid">
          <!-- Python 选择行：下拉 + 只读当前路径 -->
          <div class="row python-row">
            <div class="col">
              <!-- <label class="label">Python</label> -->
              <!-- 使用 t-select 渲染 tmpPythonPaths 列表 -->
              <t-select label="Python" v-model="settingConfig.pythonPath" :options="tmpPythonPaths" creatable filterable
                empty="No Python environment is required. Configure manually." placeholder="Select Python"
                @create="createPython" />
            </div>
          </div>
          <!-- lisa_sim Path -->
          <div class="row">
            <!-- <label class="label">lisa_sim Path</label> -->
            <t-input label="lisa_sim Path" v-model="settingConfig.homeDir" placeholder="Please select a path" style="flex: 1;">
              <!-- 在输入框右侧添加按钮 -->
              <template #suffix>
                <t-button size="small" variant="dashed" @click="selectPath">Select</t-button>
              </template>
            </t-input>
          </div>
        </div>
      </template>
    </t-dialog>
    <!-- 退出提示对话框 -->
    <t-dialog theme="danger" v-model:visible="quitDialogVisible" header="Tip" :confirm-btn="{
      content: 'Exit',
      theme: 'danger'
    }" cancel-btn="Cancel" @confirm="quitApplication">
      Do you want to exit the program?
    </t-dialog>

  </t-layout>
</template>

<script>

export default {
  name: 'MainPage',
  components: {
  },
  created() {
    this.printTestInfo();
    this.loadSettings();
    this.routerHome()
  },
  data() {
    return {
      currentMenu: 'home',
      settingConfig: {},
      collapsed: false,
      tmpPythonPaths: [],
      quitDialogVisible: false,
      settingDialogVisible: false,
      iconUrl: 'https://oteam-tdesign-1258344706.cos.ap-guangzhou.myqcloud.com/site/logo%402x.png',
      isFullScreen: false
    }
  },
  methods: {
    fullscreen() {
      this.isFullScreen = !this.isFullScreen
      window.electronAPI.fullScreen({ isFullScreen: this.isFullScreen }); // 通知主进程关闭窗口
    },
    handleItemClicked(flag) {
      this.currentMenu = flag
      if (flag == 'h5view') {
        this.$router.push("/h5view?mykey=luckey");
      }
    },
    routerHome() {
      this.currentMenu = 'home'
      this.$router.replace("/home")
    },
    changeHandler(active) {
      console.log('change', active);
      if (active == "home") {
        this.routerHome()
      } else {
        this.changePage(active)
      }
    },
    selectPath() {
      window.electronAPI.openDirectory().then((result) => {
        console.log(result);
        if (!result.canceled) {
          this.settingConfig.homeDir = result.filePaths[0];
        }
      });
    },
    quitApplication() {
      window.electronAPI.quit(); // 通知主进程关闭窗口
    },
    applySetting() {
      // this.settingConfig.darkMode ? document.documentElement.setAttribute("theme-mode", "dark") : document.documentElement.removeAttribute("theme-mode");
    },
    async printTestInfo() {
      console.log("Test Info");
    },
    saveSettings() {
      this.applySetting();
      localStorage.setItem('appSettings', JSON.stringify(this.settingConfig));
      this.settingDialogVisible = false
    },
    // true 代表数据加载成功
    async loadSettings() {
      // 是否第一次打开程序
      const firstOpen = localStorage.getItem('isInitSettings');
      if (firstOpen === null) {
        localStorage.setItem('isInitSettings', 'false');
        // 初始化设置数据
        localStorage.setItem('appSettings', JSON.stringify({
          pythonPath: '',
          homeDir: '',
        }));
        this.readSettings();
        return true;
      } else {
        this.readSettings();
      }

      // 应用设置
      this.applySetting();

      // 扫描本地所有的 Python 环境
      var paths = await window.electronAPI.searchPythonPaths();
      console.log(paths);

      this.tmpPythonPaths = paths.map(p => ({
        value: p,
        label: p,
      }));
      return true;
    },
    // 设置重置
    resetSettings() {
      localStorage.removeItem('appSettings');
      localStorage.removeItem('isInitSettings');
      this.loadSettings();
    },
    createPython(value) {
      this.tmpPythonPaths.push({
        value,
        label: value,
      });
    },
    readSettings() {
      const savedSettings = localStorage.getItem('appSettings');
      if (savedSettings) {
        this.settingConfig = JSON.parse(savedSettings);
      }
    },
    changePage(active) {
      if (active == 'h5view') {
        this.$router.push("/h5view");
      } else {
        this.$router.push(`/${active}`);
      }
    }
  }
}
</script>

<style>
.settings-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-width: 300px;
  /* 根据需要调整对话框宽度 */
}

.row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.python-row {
  align-items: flex-start;
}

.col {
  flex: 1 1 50%;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.label {
  font-size: 13px;
  color: #333;
}

.fade-enter-active {
  transition: all 0.55s cubic-bezier(0.22, 0.61, 0.36, 1);
}

.fade-leave-active {
  /* transition: all 0.55s cubic-bezier(0.22, 0.61, 0.36, 1); */
}

.fade-enter-from {
  opacity: 0;
  transform: translateX(60px);
}

.fade-leave-to {
  opacity: 0;
}

.fade-enter-to,
.fade-leave-from {
  opacity: 1;
}

* {
  font-family: 'Arial', sans-serif;
}
</style>
