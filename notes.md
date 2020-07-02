* Since no control over simulation environment, actions have to be processed in real time. 
 * Due to this, a policy update mid-episode may be fatal to the learning process.
   * Stable baselines doesn't support changing update intervals. Must create custom extension. 
 * Image pipeline must be able to process  real-time. 
   * Unknown if stability matters. 
   * Possible to defer reward extraction to policy update time. 
    * Just reward survival 
   * Could use external OCR, but too slow. 