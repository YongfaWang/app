<template>
  <t-layout style="height: 100%">
    <t-header v-if="isHiddenExecute">
      <span style="font-size: 13pt; font-weight: bold">Orbits Configure</span>
    </t-header>
    <t-content style="height: 100%">
      <div style="padding: 15px; height: calc(100% - 46px)">
        <t-form
          :data="localContent"
          label-width="120px"
          layout="vertical"
          style="height: calc(100% - 64px); overflow-y: scroll"
        >
          <t-card
            v-for="(value1, key1) in Object.getOwnPropertyNames(localContent)"
            :title="formatName(value1)"
            :key="key1"
            hover-shadow
            style="margin-bottom: 20px"
          >
            <t-form-item
              v-for="(value, key) in localContent[value1]"
              :key="key"
              :label="formatName(key)"
            >
              <t-input v-model="localContent[value1][key]" />
            </t-form-item>
          </t-card>
        </t-form>

        <div
          style="
            background-color: white;
            padding: 20px;
            display: flex;
            justify-content: end;
          "
        >
          <t-button
            v-if="!isHiddenExecute"
            @click="handlerCancel"
            shape="rectangle"
            theme="defult"
            style="margin-right: 20px"
          >
            Cancel
          </t-button>
          <t-button @click="handlerSr" shape="rectangle" theme="primary">
            Save & Run
          </t-button>
        </div>
      </div>
    </t-content>
  </t-layout>
</template>

<script>
export default {
  name: "IniConfig",
  props: {
    content: Object,
    isHiddenExecute: {
      type: Boolean,
      default: false,
    },
  },
  components: {},
  created() {},
  data() {
    return {
      localContent: {},
    };
  },
  watch: {
    content: {
      handler(newVal) {
        this.localContent = JSON.parse(JSON.stringify(newVal));
      },
      deep: true,
    },
  },
  methods: {
    formatName(str) {
      return str
        .split("_")
        .map(
          (word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
        )
        .join(" ");
    },
    handlerCancel() {
      this.$emit("onCancel");
    },
    handlerSr() {
      this.$emit("onSaveAndRun", this.localContent);
    },
    handlerOnlySave() {
      this.$emit("onOnlySave", this.localContent);
    },
  },
};
</script>

<style>
</style>
