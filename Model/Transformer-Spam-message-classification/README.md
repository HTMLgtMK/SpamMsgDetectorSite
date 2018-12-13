copy from [Transformer-Spam-message-classification](https://github.com/guojm14/Transformer-Spam-message-classification)

**Modified:**
`model_with_reference.py` add code:
```python
    def __call__():
        # .. omit

    def inferenceAPI(self,data):
        vec=np.array([self.vecmodel(data)])
        padnum=np.ones((1,vec.shape[0]))
        logit =self.sess.run(self.outlabel,feed_dict={self.inputdata:vec,self.inputpadding:padnum,self.pos:model_utils.get_position_encoding(len(vec),32)})[0]
        return logit # just return result
        
# a=inference()
# a("dsadasd")

```

**NewFile** 
`runAPI.py`
