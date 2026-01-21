<template>
  <t-layout>
    <t-header>
      <t-row>
        <t-col v-if="isHiddenExecute">
          <span style="font-size: 13pt; font-weight: bold">GW Response Configure</span>
        </t-col>
        <t-col>
        </t-col>
      </t-row>
    </t-header>
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
export default {
  name: 'GWResponse',
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
  }
}
</script>
<style></style>