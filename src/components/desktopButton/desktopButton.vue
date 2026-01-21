<template>
  <t-tooltip :content="tooltip">
    <t-image shape="round" :src="iconSrc" class="buttonIcon" v-on:click="clickHandler" />
    <t-layout style="margin-top: 1.5vh; font-weight: bold;">{{ content }}</t-layout>
  </t-tooltip>
</template>

<script>
export default {
  name: 'DesktopButton',
  props: {
    tooltip: {
      type: String,
      default: "按钮"
    },
    content: {
      type: String,
      default: "按钮"
    },
    iconSrc: {
      type: String,
      default: "https://tdesign.gtimg.com/demo/demo-image-1.png"
    }
  },
  components: {
    // echartsSample
  },
  created() {
    console.log("Home 页面加载");

  },
  data() {
    return {
    }
  },
  methods: {
    clickHandler() {
      this.$emit("onClick")
    }
  }
}
</script>

<style>
.buttonIcon{
  height: 100%;
  width: 100%;
  border-radius: 2vh;
  box-shadow: var(--td-shadow-2);
  transition: filter .2s;
}
.buttonIcon:hover {
  filter: brightness(1.10);
  transition: filter .2s;
  cursor: pointer;
}

.buttonIcon:active {
  filter: brightness(.9);
  transition: filter .2s;
  cursor: pointer;
}

img {
  -webkit-user-drag: none;
  -moz-user-drag: none;
  -ms-user-drag: none;
  user-drag: none;
}
</style>
