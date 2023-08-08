/*
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
*/
package com.ibm.research.drl.dpt.providers.masking;

import com.ibm.research.drl.dpt.configuration.MaskingConfiguration;
import com.ibm.research.drl.dpt.managers.CreditCardManager;
import com.ibm.research.drl.dpt.managers.CreditCardTypeManager;
import com.ibm.research.drl.dpt.models.CreditCard;
import com.ibm.research.drl.dpt.providers.ProviderType;

import java.security.SecureRandom;

public class CreditCardTypeMaskingProvider implements MaskingProvider {
    private static final CreditCardTypeManager ccTypeManager = CreditCardTypeManager.getInstance();
    private static final CreditCardManager creditCardManager = CreditCardManager.getInstance();

    /**
     * Instantiates a new Credit card type masking provider.
     */
    public CreditCardTypeMaskingProvider() {

    }

    /**
     * Instantiates a new Credit card type masking provider.
     *
     * @param random        the random
     * @param configuration the configuration
     */
    public CreditCardTypeMaskingProvider(SecureRandom random, MaskingConfiguration configuration) {

    }

    @Override
    public String maskLinked(String identifier, String maskedValue, ProviderType providerType) {
        CreditCard creditCard = creditCardManager.lookupInfo(maskedValue);

        if (creditCard == null) {
            return mask(identifier);
        }

        return creditCard.getName();
    }

    @Override
    public String mask(String identifier) {
        return ccTypeManager.getRandomKey();
    }
}

