<template>
  <t-layout style="height: 100%;">
    <t-header>
      <t-head-menu value="item1" height="120px">
        <template #logo>
          <img width="136" class="logo" src="https://www.tencent.com/img/index/menu_logo_hover.png" alt="logo" />
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
      <t-aside style="border-top: 1px solid var(--component-border)">
        <t-menu theme="light" v-model="currentMenu" :collapsed="collapsed" @change="changeHandler">
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
              Test1
            </t-menu-item>
            <t-menu-item value="2-3">
              <template #icon>
                <t-icon name="root-list" />
              </template>
              Test2
            </t-menu-item>
            <t-menu-item value="2-4">
              <template #icon>
                <t-icon name="check" />
              </template>
              Test3
            </t-menu-item>
          </t-menu-group>
          <t-menu-group title="More">
            <t-menu-item value="item4">
              <template #icon>
                <t-icon name="help" />
              </template>
              Guide
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
        <t-footer>Copyright @ 2019-{{ new Date().getFullYear() }} [---------------]. All Rights Reserved</t-footer>
      </t-layout>
    </t-layout>
    <t-dialog placement="center" v-model:visible="quitDialogVisible" theme="warning" header="Tip"
      body="Do you want to exit?" cancelBtn="Cancel" confirmBtn="Exit" @confirm="quitApplication" /> <t-dialog
      placement="center" v-model:visible="settingDialogVisible" header="Settings" @confirm="applySetting">
      <div>
        <p>Dark Mode</p>
        <t-switch v-model="darkMode" @change="darkModeChange" />
      </div>
      <div>
        <span>Python</span>
        <t-input abel="Name" />
      </div>
    </t-dialog>
  </t-layout>
</template>

<script>

import { ipcRenderer } from 'electron'
export default {
  name: 'MainPage',
  components: {
  },
  created() {
    this.printTestInfo();
    this.routerHome()
  },
  data() {
    return {
      currentMenu: 'home',
      darkMode: false,
      collapsed: false,
      quitDialogVisible: false,
      settingDialogVisible: false,
      iconUrl: 'https://oteam-tdesign-1258344706.cos.ap-guangzhou.myqcloud.com/site/logo%402x.png',
      isFullScreen: false
    }
  },
  methods: {
    fullscreen() {
      this.isFullScreen = !this.isFullScreen

      ipcRenderer.send('fullScreen', { isFullScreen: this.isFullScreen }); // 通知主进程关闭窗口
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
    quitApplication() {
      ipcRenderer.send('quit'); // 通知主进程关闭窗口
    },
    applySetting() {

    },
    async printTestInfo() {
    },
    darkModeChange(status) {
      if (status) {
        // 设置深色模式
        document.documentElement.setAttribute("theme-mode", "dark");
      } else {
        // 重置为浅色模式
        document.documentElement.removeAttribute("theme-mode");
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

body {
  /* background-image: url('/src/assets/bg.jpg'); */
}

/* .t-layout {
  background-color: rgba(255, 255, 255, 0);
} */

/* .t-default-menu {
  background-color: rgba(255, 255, 255, .5);
}
.t-layout__sider {
  background-color: rgba(255, 255, 255, .5);
} */
 * {
    font-family: 'Arial', sans-serif;
}
</style>
