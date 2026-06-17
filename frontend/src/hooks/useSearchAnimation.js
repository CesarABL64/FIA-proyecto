import { useState, useRef, useCallback } from 'react'

export function useSearchAnimation(steps = []) {
  const [currentStep, setCurrentStep] = useState(0)
  const [isPlaying, setIsPlaying] = useState(false)
  const [speed, setSpeed] = useState(500)
  const intervalRef = useRef(null)

  const play = useCallback(() => {
    setIsPlaying(true)
  }, [])

  const pause = useCallback(() => {
    setIsPlaying(false)
    if (intervalRef.current) {
      clearInterval(intervalRef.current)
      intervalRef.current = null
    }
  }, [])

  const stepForward = useCallback(() => {
    setCurrentStep((prev) => Math.min(prev + 1, steps.length - 1))
  }, [steps.length])

  const stepBackward = useCallback(() => {
    setCurrentStep((prev) => Math.max(prev - 1, 0))
  }, [])

  const goToStep = useCallback((step) => {
    setCurrentStep(step)
  }, [])

  const reset = useCallback(() => {
    pause()
    setCurrentStep(0)
  }, [pause])

  const setSpeedValue = useCallback((newSpeed) => {
    setSpeed(newSpeed)
  }, [])

  return {
    currentStep,
    isPlaying,
    speed,
    play,
    pause,
    stepForward,
    stepBackward,
    goToStep,
    reset,
    setSpeed: setSpeedValue,
    totalSteps: steps.length,
  }
}