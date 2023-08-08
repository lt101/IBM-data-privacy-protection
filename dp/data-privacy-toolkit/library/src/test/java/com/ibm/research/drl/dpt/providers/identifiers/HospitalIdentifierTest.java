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
package com.ibm.research.drl.dpt.providers.identifiers;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertTrue;

public class HospitalIdentifierTest {

    @Test
    public void testIdentifier() {
        Identifier identifier = new HospitalIdentifier();

        String hospitalName = "York Hospital";
        assertTrue(identifier.isOfThisType(hospitalName));

        hospitalName = "york hospital";
        assertTrue(identifier.isOfThisType(hospitalName));
    }

    @Test
    public void testIdentifierGreek() {
        Identifier identifier = new HospitalIdentifier();

        String hospitalName = "ΠΕΠΑΓΝΗ";
        assertTrue(identifier.isOfThisType(hospitalName));
    }
}
