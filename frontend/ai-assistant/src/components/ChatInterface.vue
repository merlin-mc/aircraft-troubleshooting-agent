<template>
  <div class="chat-container">
    <!-- 顶部导航栏 -->
    <div class="chat-header">
      <h1>🤖 AI 智能助手</h1>
      <button @click="clearChat" class="clear-btn">清空对话</button>
    </div>

    <!-- 消息列表区域 -->
    <div class="messages-container" ref="messagesContainer" @scroll="handleScroll">
      <!-- 空状态欢迎页 -->
      <div v-if="messages.length === 0" class="welcome-message">
        <div class="welcome-icon">👋</div>
        <h2>欢迎使用 AI 智能助手</h2>
        <p>有什么我可以帮助你的吗？</p>
      </div>

      <!-- 消息列表 -->
      <div
          v-for="(message, index) in messages"
          :key="index"
          :class="['message', `message-${message.role}`]"
      >
        <!-- 头像 -->
        <div class="message-avatar">
          {{ message.role === 'user' ? '👤' : '🤖' }}
        </div>

        <!-- 消息内容 -->
        <div class="message-content">
          <!-- AI 消息：包含思考过程和回答 -->
          <template v-if="message.role === 'assistant'">
            <!-- 思考过程区域 -->
            <div v-if="message.thinking" class="thinking-content">
              <div class="thinking-header">💭 思考过程</div>
              <div class="message-text thinking-text" v-html="message.thinking"></div>
            </div>
            <!-- 回答内容 -->
            <div class="message-text" v-html="message.answer"></div>
          </template>

          <!-- 用户消息 -->
          <template v-else>
            <div class="message-text" v-html="message.content"></div>
          </template>

          <!-- 打字动画指示器 -->
          <div v-if="message.isStreaming" class="typing-indicator">
            <span></span><span></span><span></span>
          </div>
        </div>
      </div>
    </div>

    <!-- 输入区域 -->
    <div class="input-container">
      <textarea
          v-model="inputMessage"
          @keydown="handleKeyDown"
          placeholder="输入消息..."
          :disabled="isStreaming"
          rows="1"
      ></textarea>
      <button @click="sendMessage" :disabled="!inputMessage.trim() || isStreaming" class="send-btn">
        {{ isStreaming ? '发送中...' : '发送' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { marked } from 'marked'

// 消息列表
const messages = ref([])
// 用户输入
const inputMessage = ref('')
// 是否正在流式接收响应
const isStreaming = ref(false)
// 消息列表 DOM 引用
const messagesContainer = ref(null)
// 用户是否手动滚动
const userScrolled = ref(false)
// 会话 ID，用于后端识别对话
const conversationId = ref(generateConversationId())

/**
 * 生成唯一的会话 ID
 */
function generateConversationId() {
  return 'conv_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9)
}

/**
 * 滚动到底部（如果用户没有手动向上滚动）
 */
const scrollToBottom = () => {
  nextTick(() => {
    if (!messagesContainer.value) return
    const { scrollTop, scrollHeight, clientHeight } = messagesContainer.value
    const isNearBottom = scrollHeight - scrollTop - clientHeight < 100
    if (isNearBottom || !userScrolled.value) {
      messagesContainer.value.scrollTop = scrollHeight
    }
  })
}

/**
 * 监听用户滚动，标记用户是否手动滚动
 */
const handleScroll = () => {
  if (!messagesContainer.value) return
  const { scrollTop, scrollHeight, clientHeight } = messagesContainer.value
  userScrolled.value = scrollHeight - scrollTop - clientHeight >= 100
}

/**
 * 解析消息内容，分离思考过程和回答内容
 * @param {string} content - 原始消息内容
 * @returns {{ thinking: string, answer: string }} 分离后的思考和回答
 */
const parseMessage = (content) => {
  // 检查是否有完整的思考标签
  const thinkMatch = content.match(/<think>([\s\S]*?)<\/think>/)
  if (thinkMatch) {
    return {
      thinking: marked.parse(thinkMatch[1].trim()),
      answer: marked.parse(content.replace(/<think>[\s\S]*?<\/think>/, '').trim())
    }
  }
  // 检查是否有未闭合的思考标签（流式传输中）
  if (content.includes('<think>') && !content.includes('</think>')) {
    return {
      thinking: marked.parse(content.match(/<think>([\s\S]*)/)[1]),
      answer: ''
    }
  }
  // 无思考过程，直接返回
  return {
    thinking: '',
    answer: marked.parse(content)
  }
}

/**
 * 发送消息给后端 AI 接口
 */
const sendMessage = async () => {
  // 防止空消息或重复发送
  if (!inputMessage.value.trim() || isStreaming.value) return

  // 获取并清空输入框
  const userMessage = inputMessage.value.trim()
  inputMessage.value = ''

  // 添加用户消息到列表
  messages.value.push({
    role: 'user',
    content: marked.parse(userMessage),
    timestamp: new Date()
  })
  scrollToBottom()

  // 添加 AI 消息占位符（初始为空）
  messages.value.push({
    role: 'assistant',
    content: '',
    thinking: '',
    answer: '',
    timestamp: new Date(),
    isStreaming: true
  })

  // 标记正在流式接收
  isStreaming.value = true

  try {
    // 发送请求到后端流式接口
    const response = await fetch(
      `http://localhost:8080/chat/stream?message=${encodeURIComponent(userMessage)}&conversationId=${encodeURIComponent(conversationId.value)}`,
      { method: 'GET' }
    )

    // 检查响应状态
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    // 获取响应体的读取器（用于流式读取）
    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let fullContent = ''

    // 流式读取响应数据
    while (true) {
      // 读取下一个数据块
      const { done, value } = await reader.read()
      if (done) break

      // 解码数据块并追加到完整内容
      fullContent += decoder.decode(value, { stream: true })

      // 解析消息内容（分离思考过程和回答）
      const parsed = parseMessage(fullContent)

      // 更新最后一条 AI 消息
      const lastMessage = messages.value[messages.value.length - 1]
      if (lastMessage?.role === 'assistant') {
        lastMessage.content = fullContent
        lastMessage.thinking = parsed.thinking
        lastMessage.answer = parsed.answer
        scrollToBottom()
      }
    }

    // 流式读取完成，标记响应结束
    const finalMessage = messages.value[messages.value.length - 1]
    if (finalMessage?.role === 'assistant') {
      finalMessage.isStreaming = false
    }

  } catch (error) {
    // 处理请求错误
    console.error('Error sending message:', error)
    const lastMessage = messages.value[messages.value.length - 1]
    if (lastMessage?.role === 'assistant') {
      lastMessage.content = '抱歉，发生了错误。请确保后端服务正在运行。'
      lastMessage.answer = marked.parse('抱歉，发生了错误。请确保后端服务正在运行。')
      lastMessage.isStreaming = false
    }

  } finally {
    // 无论成功或失败，都需要重置状态
    isStreaming.value = false
    userScrolled.value = false
  }
}

/**
 * 处理键盘事件，支持 Enter 发送消息
 */
const handleKeyDown = (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    sendMessage()
  }
}

/**
 * 清空对话并生成新的会话 ID
 */
const clearChat = () => {
  messages.value = []
  conversationId.value = generateConversationId()
}
</script>

<style scoped>
/* 整体容器 */
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  max-width: 1200px;
  margin: 0 auto;
  background: #ffffff;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
}

/* 顶部导航栏 */
.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 30px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.chat-header h1 {
  font-size: 24px;
  font-weight: 600;
}

/* 清空按钮 */
.clear-btn {
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.2);
  border: none;
  border-radius: 8px;
  color: white;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.3s;
}

.clear-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* 消息列表容器 */
.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 30px;
  background: #f5f5f5;
}

/* 空状态欢迎页 */
.welcome-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
  color: #666;
}

.welcome-icon {
  font-size: 64px;
  margin-bottom: 20px;
}

.welcome-message h2 {
  font-size: 24px;
  margin-bottom: 10px;
  color: #333;
}

/* 消息通用样式 */
.message {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

/* 用户消息靠右 */
.message-user {
  flex-direction: row-reverse;
}

/* 头像 */
.message-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
}

/* AI 头像渐变背景 */
.message-assistant .message-avatar {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

/* 消息内容气泡 */
.message-content {
  max-width: 70%;
  padding: 15px 20px;
  border-radius: 15px;
  line-height: 1.6;
}

/* 用户消息气泡 */
.message-user .message-content {
  background: #667eea;
  color: white;
  border-bottom-right-radius: 5px;
}

/* AI 消息气泡 */
.message-assistant .message-content {
  background: white;
  color: #333;
  border-bottom-left-radius: 5px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 消息文本 */
.message-text {
  white-space: pre-wrap;
  word-break: break-word;
}

/* Markdown 渲染样式 */
.message-text :deep(strong) {
  font-weight: 600;
}

.message-text :deep(code) {
  background: rgba(0, 0, 0, 0.08);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 0.9em;
}

.message-text :deep(p) {
  margin: 0 0 10px 0;
}

.message-text :deep(p:last-child) {
  margin-bottom: 0;
}

/* 思考过程区域 */
.thinking-content {
  margin-bottom: 15px;
  padding: 12px 15px;
  background: #f8f8f8;
  border-radius: 10px;
  border-left: 3px solid #667eea;
}

.thinking-header {
  font-size: 12px;
  color: #888;
  margin-bottom: 8px;
  font-weight: 500;
}

.thinking-text {
  color: #888 !important;
  font-size: 14px;
}

.thinking-text :deep(p) {
  margin: 0 0 8px 0;
}

.thinking-text :deep(p:last-child) {
  margin-bottom: 0;
}

/* 打字动画 */
.typing-indicator {
  display: inline-flex;
  gap: 4px;
  padding: 10px 0;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background: #667eea;
  border-radius: 50%;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.4;
  }
  30% {
    transform: translateY(-10px);
    opacity: 1;
  }
}

/* 输入区域 */
.input-container {
  display: flex;
  gap: 15px;
  padding: 20px 30px;
  background: white;
  border-top: 1px solid #e0e0e0;
}

.input-container textarea {
  flex: 1;
  padding: 15px 20px;
  border: 2px solid #e0e0e0;
  border-radius: 25px;
  resize: none;
  font-size: 16px;
  font-family: inherit;
  outline: none;
  transition: border-color 0.3s;
}

.input-container textarea:focus {
  border-color: #667eea;
}

.input-container textarea:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
}

/* 发送按钮 */
.send-btn {
  padding: 15px 30px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 25px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.3s, transform 0.3s;
}

.send-btn:hover:not(:disabled) {
  opacity: 0.9;
  transform: scale(1.02);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 响应式布局 */
@media (max-width: 768px) {
  .message-content {
    max-width: 85%;
  }

  .input-container,
  .chat-header {
    padding: 15px 20px;
  }
}
</style>
