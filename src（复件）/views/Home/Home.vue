<template>
  <div style="height: 100%; width: 100%; min-width: 900px; min-height: 300px;">
    <div style="position: relative; top: calc((7vh + 2vh + 7vh + 7vh +1.5vh));">
      <t-row justify="center" :gutter="[
        { xs: 8, sm: 16, md: 24, lg: 32, xl: 32, xxl: 40 },
        { xs: 8, sm: 16, md: 24, lg: 32, xl: 32, xxl: 40 },
      ]">
        <t-col>
          <div class="button-wh">
            <DesktopButton tooltip="点击后进行Orbits操作" content="Orbits" @onClick="pageRouter('orbits')"></DesktopButton>
          </div>
        </t-col>
        <t-col>
          <!-- <SwapRightIcon /> -->
          <svg xmlns="http://www.w3.org/2000/svg" width="7vh" height="7vh" style="min-width: 100px; min-height: 100px;"
            viewBox="0 0 24 24">
            <path fill="currentColor"
              d="M4.5 11h11.586l-4.5-4.5L13 5.086L19.914 12L13 18.914L11.586 17.5l4.5-4.5H4.5z" />
          </svg>
        </t-col>
        <t-col>
          <div class="button-wh">
            <DesktopButton tooltip="点击后进行GW Response操作" content="GW Response" @onClick="pageRouter('gwresponse')"></DesktopButton>
          </div>
        </t-col>
        <t-col>
          <!-- <SwapRightIcon /> -->
          <svg xmlns="http://www.w3.org/2000/svg" width="7vh" height="7vh" style="min-width: 100px; min-height: 100px;"
            viewBox="0 0 24 24">
            <path fill="currentColor"
              d="M4.5 11h11.586l-4.5-4.5L13 5.086L19.914 12L13 18.914L11.586 17.5l4.5-4.5H4.5z" />
          </svg>
        </t-col>
        <t-col>
          <div class="button-wh">
            <DesktopButton tooltip="点击后进行Instrument操作" content="Instrument" @onClick="pageRouter('instrument')"></DesktopButton>
          </div>
        </t-col>
        <t-col>
          <!-- <SwapRightIcon /> -->
          <svg xmlns="http://www.w3.org/2000/svg" width="7vh" height="7vh" style="min-width: 100px; min-height: 100px;"
            viewBox="0 0 24 24">
            <path fill="currentColor"
              d="M4.5 11h11.586l-4.5-4.5L13 5.086L19.914 12L13 18.914L11.586 17.5l4.5-4.5H4.5z" />
          </svg>
        </t-col>
        <t-col>
          <div class="button-wh">
            <DesktopButton tooltip="点击后进行H5 View操作" content="H5 View" @onClick="pageRouter('h5view')"></DesktopButton>
          </div>
        </t-col>
      </t-row>

      <t-row justify="center" style="margin-top: 2vh;" :gutter="[
        { xs: 8, sm: 16, md: 24, lg: 32, xl: 32, xxl: 40 },
        { xs: 8, sm: 16, md: 24, lg: 32, xl: 32, xxl: 40 },
      ]">
        <t-col>

          <div class="button-wh"></div>
        </t-col>
        <t-col>
          <!-- <SwapRightIcon /> -->
          <div class="button-wh"></div>
        </t-col>
        <t-col>
          <div class="button-wh">
          </div>
        </t-col>
        <t-col>
          <!-- <SwapRightIcon /> -->
          <div class="button-wh"></div>
        </t-col>
        <t-col>
          <div class="button-wh">
            <svg xmlns="http://www.w3.org/2000/svg" width="7vh" height="7vh"
              style="min-width: 100px; min-height: 100px;" viewBox="0 0 24 24">
              <path fill="currentColor"
                d="M11 19.5V7.914l-4.5 4.5L5.086 11L12 4.086L18.914 11L17.5 12.414l-4.5-4.5V19.5z" />
            </svg>
          </div>
        </t-col>
        <t-col>
          <!-- <SwapRightIcon /> -->
          <div class="button-wh"></div>
        </t-col>
        <t-col>
          <!-- <SwapRightIcon /> -->
          <div class="button-wh"></div>
        </t-col>
      </t-row>

      <t-row justify="center" :gutter="[
        { xs: 8, sm: 16, md: 24, lg: 32, xl: 32, xxl: 40 },
        { xs: 8, sm: 16, md: 24, lg: 32, xl: 32, xxl: 40 },
      ]">
        <t-col>

          <div class="button-wh"></div>
        </t-col>
        <t-col>
          <!-- <SwapRightIcon /> -->

          <div class="button-wh"></div>
        </t-col>
        <t-col>
          <div class="button-wh">
          </div>
        </t-col>
        <t-col>
          <!-- <SwapRightIcon /> -->
          <div class="button-wh"></div>
        </t-col>
        <t-col>
          <div class="button-wh">
            <div class="button-wh">
              <DesktopButton tooltip="点击后进行Glitchs操作" content="Glitchs" @onClick="pageRouter('glitchs')"></DesktopButton>
            </div>
          </div>
        </t-col>
        <t-col>
          <!-- <SwapRightIcon /> -->
          <div class="button-wh"></div>
        </t-col>
        <t-col>
          <!-- <SwapRightIcon /> -->
          <div class="button-wh"></div>
        </t-col>
      </t-row>
    </div>
    <div>
      <t-dialog placement="center" v-model:visible="winconfig.workWeiget.isShow" :header="getCurrentWeightName" :confirmBtn="null" :cancelBtn="null">
        <div>
          <H5View @onCancel="winconfig.workWeiget.isShow = false" v-if="this.winconfig.flag == 'h5view'"/>
          <Glitchs @onCancel="winconfig.workWeiget.isShow = false" v-else-if="this.winconfig.flag === 'glitchs'"/>
          <GWResponse @onCancel="winconfig.workWeiget.isShow = false" v-else-if="this.winconfig.flag === 'gwresponse'"/>
          <Instrument @onCancel="winconfig.workWeiget.isShow = false" v-else-if="this.winconfig.flag === 'instrument'"/>
          <Orbits @onCancel="winconfig.workWeiget.isShow = false" v-else-if="this.winconfig.flag === 'orbits'"/>
        </div>
      </t-dialog>
    </div>
  </div>
</template>

<script>
import DesktopButton from '@/components/desktopButton/desktopButton';
import H5View from '@/views/H5View/H5View';
import Glitchs from '@/views/Glitchs/Glitchs';
import GWResponse from '@/views/GWResponse/GWResponse';
import Instrument from '@/views/Instrument/Instrument';
import Orbits from '@/views/Orbits/Orbits';
export default {
  name: 'Home-a',
  components: {
    DesktopButton,
    H5View,
    Glitchs,
    GWResponse,
    Instrument,
    Orbits
  },
  setup() {
  },
  created() {
    console.log("Home 页面加载");

  },
  data() {
    return {
      winconfig: {
        workWeiget: {
          isShow: false,
          flag: ""
        }
      }
    }
  },
  methods: {
    pageRouter(flag) {
      this.winconfig.flag = flag
      this.winconfig.workWeiget.isShow = true
    },
    getCurrentWeightName() {
        switch (this.winconfig.flag) {
          case 'h5view':
            return "H5View"
          case 'glitchs':
            return "Glitchs Configure"
          case 'gwresponse':
            return "GW Response Configure"
          case 'instrument':
            return "Instrument Configure"
          case 'orbits':
            return "Orbits Configure"
        }
    }
  }
}
</script>

<style>
.button-wh {
  width: 10vh;
  height: 10vh;
  min-width: 100px;
  min-height: 100px;
}
</style>
