<ul>
  <li> rozpoznawanie-plci-z-obrazu</li>
  <li>The algorithm uses a neural network.</li>
  <li>The file "uczenie_sieci.py" reads a split image database by gender. Each sample of an individual image is normalised to a range from 0 to 1.</li>
  <li>The normalized image samples go to the network input.</li>
  <li>The "test_sieci_neu.py" file reads the test image database and normalizes the image samples.</li>
  <li>Predictions for the image are made from the samples.</li>
  <li>If the network for a given image responds with 0, there is a woman in the image if 1 is a man.</li>
</ul>
