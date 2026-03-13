<template>
  <div class="item-scan">
    <van-nav-bar
      title="扫描添加物品"
      left-arrow
      @click-left="$router.back()"
    />
    
    <!-- 扫描模式选择 -->
    <div class="scan-modes">
      <van-tabs v-model:active="activeMode" type="card">
        <van-tab title="📷 拍照识别" name="camera">
          <div class="camera-section">
            <div class="camera-preview" @click="takePhoto">
              <van-icon name="photograph" size="60" color="#999" />
              <p>点击拍照或从相册选择</p>
            </div>
            <input 
              ref="fileInput"
              type="file" 
              accept="image/*" 
              capture="environment"
              style="display: none"
              @change="handleFileChange"
            />
          </div>
        </van-tab>
        
        <van-tab title="📱 AR扫描" name="ar">
          <div class="ar-section">
            <div class="ar-preview">
              <van-icon name="aim" size="60" color="#1989fa" />
              <p>AR物体识别</p>
              <van-button type="primary" @click="startARScan">
                启动AR扫描
              </van-button>
            </div>
          </div>
        </van-tab>
        
        <van-tab title="🔊 语音录入" name="voice">
          <div class="voice-section">
            <div class="voice-recorder" @click="toggleRecording">
              <div class="voice-icon" :class="{ recording: isRecording }">
                <van-icon :name="isRecording ? 'stop-circle-o' : 'volume-o'" size="50" />
              </div>
              <p>{{ isRecording ? '点击停止录音' : '点击开始语音录入' }}</p>
            </div>
            <div v-if="voiceText" class="voice-result">
              <van-field
                v-model="voiceText"
                label="识别结果"
                type="textarea"
                rows="3"
                placeholder="语音识别内容..."
              />
            </div>
          </div>
        </van-tab>
        
        <van-tab title="⌨️ 手动录入" name="manual">
          <div class="manual-section">
            <van-form @submit="onSubmit">
              <van-field
                v-model="form.name"
                name="name"
                label="物品名称"
                placeholder="请输入物品名称"
                :rules="[{ required: true, message: '请填写物品名称' }]"
              />
              <van-field
                v-model="form.category"
                name="category"
                label="类别"
                placeholder="选择类别"
                readonly
                @click="showCategoryPicker = true"
              />
              <van-field
                v-model="form.price"
                name="price"
                label="价格"
                placeholder="请输入价格"
                type="number"
              />
              <van-field
                v-model="form.purchaseDate"
                name="purchaseDate"
                label="购买日期"
                placeholder="选择日期"
                readonly
                @click="showDatePicker = true"
              />
              <van-field
                v-model="form.location"
                name="location"
                label="存放位置"
                placeholder="如：客厅、卧室"
              />
              <van-field
                v-model="form.notes"
                name="notes"
                label="备注"
                type="textarea"
                rows="2"
                placeholder="其他信息..."
              />
              
              <div style="margin: 16px;">
                <van-button round block type="primary" native-type="submit">
                  保存物品
                </van-button>
              </div>
            </van-form>
          </div>
        </van-tab>
      </van-tabs>
    </div>
    
    <!-- 类别选择器 -->
    <van-popup v-model:show="showCategoryPicker" position="bottom">
      <van-picker
        :columns="categories"
        @confirm="onCategoryConfirm"
        @cancel="showCategoryPicker = false"
      />
    </van-popup>
    
    <!-- 日期选择器 -->
    <van-popup v-model:show="showDatePicker" position="bottom">
      <van-date-picker
        @confirm="onDateConfirm"
        @cancel="showDatePicker = false"
      />
    </van-popup>
    
    <!-- 识别结果预览 -->
    <van-dialog v-model:show="showScanResult" title="识别结果" show-cancel-button @confirm="confirmScan">
      <div class="scan-result">
        <van-image
          v-if="capturedImage"
          width="100%"
          height="200"
          fit="cover"
          :src="capturedImage"
        />
        <van-cell-group>
          <van-cell title="识别物品" :value="scanResult.name || '未识别'" />
          <van-cell title="置信度" :value="scanResult.confidence || '-'" />
          <van-cell title="建议分类" :value="scanResult.category || '-'" />
        </van-cell-group>
      </div>
    </van-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { showToast, showLoadingToast, closeToast } from 'vant';

const router = useRouter();
const fileInput = ref(null);
const activeMode = ref('camera');

// 拍照相关
const capturedImage = ref('');
const showScanResult = ref(false);
const scanResult = reactive({
  name: '',
  confidence: '',
  category: ''
});

// 语音录入
const isRecording = ref(false);
const voiceText = ref('');

// 手动录入表单
const form = reactive({
  name: '',
  category: '',
  price: '',
  purchaseDate: '',
  location: '',
  notes: ''
});

const showCategoryPicker = ref(false);
const showDatePicker = ref(false);

const categories = [
  { text: '家具', value: 'furniture' },
  { text: '电子产品', value: 'electronics' },
  { text: '书籍', value: 'books' },
  { text: '衣物', value: 'clothing' },
  { text: '装饰品', value: 'decorations' },
  { text: '厨房用品', value: 'kitchen' },
  { text: '运动器材', value: 'sports' },
  { text: '其他', value: 'others' }
];

// 拍照
const takePhoto = () => {
  fileInput.value.click();
};

// 处理文件选择
const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (!file) return;
  
  // 读取图片
  const reader = new FileReader();
  reader.onload = (e) => {
    capturedImage.value = e.target.result;
    performRecognition();
  };
  reader.readAsDataURL(file);
};

// 执行图像识别（模拟）
const performRecognition = () => {
  showLoadingToast({
    message: '识别中...',
    forbidClick: true,
  });
  
  // 模拟API调用
  setTimeout(() => {
    closeToast();
    
    // 模拟识别结果
    const mockResults = [
      { name: '皮质沙发', confidence: '92%', category: '家具' },
      { name: '液晶电视机', confidence: '88%', category: '电子产品' },
      { name: '实木茶几', confidence: '85%', category: '家具' }
    ];
    
    const result = mockResults[Math.floor(Math.random() * mockResults.length)];
    scanResult.name = result.name;
    scanResult.confidence = result.confidence;
    scanResult.category = result.category;
    
    showScanResult.value = true;
  }, 2000);
};

// 确认扫描结果
const confirmScan = () => {
  // 填充表单
  form.name = scanResult.name;
  form.category = scanResult.category;
  
  showToast('识别完成，请补充信息');
  activeMode.value = 'manual';
};

// AR扫描
const startARScan = () => {
  showToast('AR扫描功能开发中');
};

// 语音录制
const toggleRecording = () => {
  isRecording.value = !isRecording.value;
  
  if (isRecording.value) {
    showToast('开始录音...');
    // 模拟录音5秒后自动停止
    setTimeout(() => {
      if (isRecording.value) {
        isRecording.value = false;
        voiceText.value = '这是一个示例语音识别结果，实际使用时需要接入语音识别API。';
        showToast('录音完成');
      }
    }, 5000);
  } else {
    showToast('录音停止');
  }
};

// 类别选择
const onCategoryConfirm = ({ selectedOptions }) => {
  form.category = selectedOptions[0].text;
  showCategoryPicker.value = false;
};

// 日期选择
const onDateConfirm = ({ selectedValues }) => {
  form.purchaseDate = selectedValues.join('-');
  showDatePicker.value = false;
};

// 提交表单
const onSubmit = () => {
  showLoadingToast({
    message: '保存中...',
    forbidClick: true,
  });
  
  // 模拟API调用
  setTimeout(() => {
    closeToast();
    showToast('物品添加成功');
    router.push('/items');
  }, 1500);
};
</script>

<style scoped>
.item-scan {
  min-height: 100vh;
  background: #f7f8fa;
}

.camera-section,
.ar-section,
.voice-section,
.manual-section {
  padding: 20px;
}

.camera-preview {
  background: #f0f0f0;
  border: 2px dashed #ccc;
  border-radius: 12px;
  height: 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.camera-preview p {
  margin-top: 10px;
  color: #666;
  font-size: 14px;
}

.ar-preview {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  height: 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: white;
}

.ar-preview p {
  margin: 10px 0;
}

.voice-recorder {
  background: white;
  border-radius: 12px;
  padding: 40px;
  text-align: center;
}

.voice-icon {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 15px;
  transition: all 0.3s;
}

.voice-icon.recording {
  background: #ff4d4f;
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.voice-result {
  margin-top: 20px;
}

.scan-result {
  padding: 16px;
}

:deep(.van-tabs__wrap) {
  padding: 0 16px;
}

:deep(.van-tabs__nav--card) {
  border: none;
}

:deep(.van-tab--card) {
  border: none;
  background: #f0f0f0;
}

:deep(.van-tab--card.van-tab--active) {
  background: #1989fa;
  color: white;
}
</style>